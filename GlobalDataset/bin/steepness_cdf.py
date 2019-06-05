import numpy as np
import dem as d
from numpy.fft import fft2, ifft2, ifftshift

def calc_cdf(ks_grids, area_grids, vmax=400, R2_cutoff = 0.0, area_cutoff = 2E6, density_weighting_distance = False):
    
    ks_vals = np.array([])
    n_vals = np.array([])
    R2_vals = np.array([])
    density_vals = np.array([])
    for (ks_grid, area_grid) in zip(ks_grids, area_grids):    
        i = np.where(~np.isnan(ks_grid._griddata) & (ks_grid._griddata >= 0) & (area_grid._griddata >= area_cutoff))
        ks_vals = np.concatenate((ks_vals, ks_grid._griddata[i]))
        n_vals = np.concatenate((n_vals, ks_grid._n[i]))
        R2_vals = np.concatenate((R2_vals, ks_grid._r2[i]))
        if density_weighting_distance is not False:
            template_grid = np.zeros_like(ks_grid._griddata)
            (ny, nx) = template_grid.shape
            (cy, cx) = (ny/2.0, nx/2.0)
            dy, dx = np.meshgrid(np.arange(0,ny)-cy, np.arange(0,nx)-cx, indexing = 'ij')
            d = np.sqrt(np.power(dx,2) + np.power(dy,2))
            j = np.where(d <= density_weighting_distance)
            template_grid[j] = 1.0
            de = area_grid._area_per_pixel()
            ks_bin = (~np.isnan(ks_grid._griddata) & (area_grid >= area_cutoff)).astype(float)*de
            template_F = fft2(template_grid)
            density_weight = np.real(ifftshift(ifft2(template_F*fft2(de))) / ifftshift(ifft2(template_F*fft2(ks_bin))))
            density_vals = np.concatenate((density_vals, density_weight[i]))
            
    i = np.where(R2_vals >= R2_cutoff)
    ks_vals = ks_vals[i]
    n_vals = n_vals[i]
    if density_weighting_distance is not False:
        density_vals = density_vals[i]
        
    i = np.argsort(ks_vals)
    ks_vals = ks_vals[i]
    n_vals = n_vals[i]
    
    weights = 1 / n_vals
    
    if density_weighting_distance is not False:
        density_vals = density_vals[i]
        weights *= density_vals
        
    bins = np.concatenate((np.array([-0.5]), np.arange(0.5, vmax, 1),np.array([vmax])+0.5, np.array([np.max(ks_vals[:])])))
    hist, _ = np.histogram(ks_vals, bins = bins, weights = weights)
    bin_centers = np.concatenate((np.arange(0,vmax,1),np.array([vmax])))
    cdf = np.cumsum(hist)
    cdf /= cdf[-1]
    cdf = cdf[0:-1]
    return bin_centers, cdf