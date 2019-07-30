import sys
import dem as d
import matplotlib.pylab as plt
import numpy as np
gridname = sys.argv[1]
sampleposition = int(sys.argv[2])
area_at_outlet = float(sys.argv[3])

counter = 0

resolutions = [90, 250, 500]

outlets = np.load(gridname + '/' + gridname + '_sample_locations.npy')
outlet = outlets[sampleposition]

for resolution in resolutions:
    elevation = d.Elevation.load(gridname + "/" + gridname + "_elevation")
    if elevation != 90:
        elevation = elevation.resample(resolution)
    fill = d.FilledElevation(elevation = elevation)
    fd = d.FlowDirectionD8(flooded_dem = fill)
    area = d.Area(flow_direction = fd)
    logarea = d.LogArea(area = area)
    outlet_ij = area._xy_to_rowscols((outlet,))
    outlet_move_ij = area.find_nearest_cell_with_value_greater_than(outlet_ij[0], area_at_outlet, 2)
    (outlet_move_xy, ) = area._rowscols_to_xy((outlet_move_ij, )) 
    
    
    plt.figure(1+counter)
    elevation.plot()
    plt.plot(outlet[0], outlet[1],'r.')
    plt.plot(outlet_move_xy[0], outlet_move_xy[1], 'g.')
    
    plt.figure(2+counter)
    area.plot(interpolation='nearest')
    plt.plot(outlet[0], outlet[1],'r.')
    plt.plot(outlet_move_xy[0], outlet_move_xy[1], 'g.')
    
    plt.figure(3+counter)
    logarea.plot(interpolation='nearest')
    plt.plot(outlet[0], outlet[1],'r.')
    plt.plot(outlet_move_xy[0], outlet_move_xy[1], 'g.')
    
    counter += 3

plt.show()
input()