import dem as d

prefixes = ['af', 'as', 'au', 'ca', 'eu', 'na', 'sa']
thetas = [0.4, 0.5, 0.6]
vertical_interval = 3.0*16.0

for prefix in prefixes:

	dem = d.Elevation.load(prefix + '_elevation')
	area = d.GeographicArea.load(prefix + '_area')
	fd = d.FlowDirectionD8.load(prefix + '_flow_direction')

	for theta in thetas:

		ks = d.GeographicKsFromChiWithSmoothing(elevation = dem, area = area, flow_direction = fd, theta = theta, vertical_interval = vertical_interval)
		ks.save(prefix + '_ks_theta_' + str(theta).replace('.','_'))

