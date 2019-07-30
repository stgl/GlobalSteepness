def resolution_test(elevation_full, outlet, area_at_outlet):
    
    import dem as d
    
    resolutions = [90, 250, 500]
    thetas = [0.4, 0.5, 0.6]
    from utils import calc_ks_for_outlet
    
    out_dict = {}
    
    for resolution in resolutions:
        if resolution != resolutions[0]:
            elevation = elevation_full.resample(resolution)
        else:
            elevation = elevation_full
        fill = d.FilledElevation(elevation = elevation)
        fd = d.FlowDirectionD8(flooded_dem = fill)
        area = d.Area(flow_direction = fd)
        out_dict[str(resolution)] = {}
        outlet_ij = area._xy_to_rowscols((outlet,))
        outlet_move_ij = area.find_nearest_cell_with_value_greater_than(outlet_ij[0], area_at_outlet, 2)
        (outlet_move_xy, ) = area._rowscols_to_xy((outlet_move_ij, )) 
        print('area: ' + str(area_at_outlet) + ', area found: ' + str(area[outlet_move_ij[0], outlet_move_ij[1]]))
        
        '''
        import matplotlib.pylab as plt
        plt.figure(1)
        elevation.plot()
        plt.plot(outlet_move_xy[0], outlet_move_xy[1],'r.');
        plt.figure(2)
        area.plot(interpolation = 'nearest')
        plt.plot(outlet_move_xy[0],outlet_move_xy[1], 'r.')
        input()
        plt.figure(1)
        plt.close()
        plt.figure(2)
        plt.close()
        '''
        
        for theta in thetas:
            (ks, R2) = calc_ks_for_outlet(outlet_move_xy, theta, elevation = elevation, flow_direction = fd, area = area, xo = 250)
            out_dict[str(resolution)][str(theta)] = {'ks': ks, 'R2': R2}
            
    return out_dict

info = {'venezuela': {'prefix': 'venezuela/venezuela',
                      'samples': ['RNF-117', 'RNF-129'],
                      'areas': [208.42E6, 684.89E6]},
        'brazil': {'prefix': 'brazil/brazil',
                   'samples': ['RS1', 'RS4', 'RS5', 'RS6', 'RS7', 'RS8'],
                   'areas': [19.9E6, 3.183E6, 11.129E6, 0.6E6, 35.373E6, 10.959E6]},
        'costarica': {'prefix': 'costarica/costarica',
                      'samples': ['Rio Cedro', 'Rio Hamaca'],
                      'areas': [43.829E6, 29.176E6]},
        'guatemala': {'prefix': 'guatemala/guatemala',
                      'samples': ['GT-62'],
                      'areas': [5.168E6]},
        'taiwan': {'prefix': 'taiwan/taiwan',
                   'samples': ['RS1', 'RS2', 'RS3'],
                   'areas': [1.393E6, 523.074E6, 535.556E6]}
        }

import dem as d
import numpy as np

results = {}
ks = {}

for site in info.keys():
    print('working on: ' + str(site))
    ks[site] = {'0_4': [],
                '0_5': [],
                '0_6': []}
    
    dem = d.Elevation.load(info[site]['prefix'] + '_elevation')
    outlets = np.load(info[site]['prefix'] + '_sample_locations.npy')
    results[site] = {}
    for (outlet, sample_name, outlet_area) in zip(outlets, info[site]['samples'], info[site]['areas']):
        print('sample name: ' + sample_name)
        #try:
        results[site][sample_name] = resolution_test(dem, outlet, outlet_area)
        ks[site]['0_4'] += [results[site][sample_name]['90']['0.4']['ks']]
        ks[site]['0_5'] += [results[site][sample_name]['90']['0.5']['ks']]
        ks[site]['0_6'] += [results[site][sample_name]['90']['0.6']['ks']]
        #except:
        #    pass
import pickle as p


p.dump(results, open('resolution_test_results.p', 'wb'))
p.dump(ks, open('ks.p', 'wb'))

resolutions = [90, 250, 500]

for resolution in resolutions:
    for site in info.keys():
        for sample in results[site].keys():
            sampleout = sample
            for theta in ['0.4', '0.5', '0.6']:
                sampleout += ', ' + str(results[site][sample][str(resolution)][theta]['ks'][0]) + ', ' + str(results[site][sample][str(resolution)][theta]['R2'][0])
            print(sampleout)
            
import matplotlib.pylab as plt

plt.show()

                
