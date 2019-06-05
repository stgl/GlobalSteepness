import dem as d

prefixes = ['as', 'af', 'au', 'ca', 'eu', 'na', 'sa']
thetas = [0.4, 0.5, 0.6]
horizontal_interval = 5000.0 

for prefix in prefixes:

	dem = d.Elevation.load(prefix + '_elevation')
	area = d.GeographicArea.load(prefix + '_area')
	fd = d.FlowDirectionD8.load(prefix + '_flow_direction')

	for theta in thetas:

		ks = d.GeographicKsFromChiWithSmoothing(elevation = dem, area = area, flow_direction = fd, theta = theta, horizontal_interval = horizontal_interval)
		ks.save(prefix + '_ks_hz_theta_' + str(theta).replace('.','_'))

