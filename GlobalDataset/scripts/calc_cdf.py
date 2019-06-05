import numpy as np

def calc_cdf(ks, area, threshold = 2E6, use_r2 = False):
    
    i = np.where(~np.isnan(ks._griddata) & (ks._griddata > 0) & (area._griddata > threshold) & (ks._pval > 0))
    bins = np.concatenate((np.arange(0, 400, 5), np.array([500000])))
    weights = 1.0 / ks._n[i]
    if use_r2:
        weights *= ks._r2[i]
    h, b = np.histogram(ks._griddata[i], bins = bins, weights = weights)
    c = np.cumsum(h)
    c = c / c[-1]
    return c, (b[0:-1] + b[1:])/2.0, h

