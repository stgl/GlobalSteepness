import matplotlib.pylab as plt
import dem as d
from steepness_cdf import calc_cdf

prefixes = ['as', 'af', 'au', 'ca', 'na', 'sa']
lines = ['k-', 'k--', 'k:', 'b-', 'b--', 'b:', 'g-']

kss = []
areas = []

plt.figure(1)

for (prefix, line) in zip(prefixes, lines):
    ks = d.GeographicKsFromChiWithSmoothing.load(prefix + '_ks_theta_0_4')
    area = d.GeographicArea.load(prefix + '_area')
    kss += [ks]
    areas += [area]
    [bins, cdf] = calc_cdf([ks], [area], R2_cutoff = 0.8)
    plt.plot(bins, cdf, line)

plt.ion()
plt.show()

plt.figure(2)

[bins, cdf] = calc_cdf(kss, areas, R2_cutoff = 0.8)
plt.plot(bins, cdf, 'k-')
plt.show()

    