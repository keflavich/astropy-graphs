import numpy as np
from astropy.table import Table
import matplotlib.pyplot as plt
from astropy.utils.console import ProgressBar

plt.rcParams['axes.prop_cycle'] = plt.cycler('color', ('#338ADD', '#9A44B6',
                                                       '#A60628', '#467821',
                                                       '#CF4457', '#188487',
                                                       '#E24A33'))

tbl = Table.read('astropy_issue_states.txt', format='ascii.fixed_width')
lifetime = np.array([x.strip(" seconds") for x in tbl['Lifetime']]).astype('float')
is_pr = tbl['Is_PR'] == 'True'

unique_labels = list(set([x for row in tbl for x in str(row['Labels']).split(",")]))

plt.figure(1).clf()
logdaybins = np.logspace(1-5, 8.25-5)
plt.hist(lifetime/86400, bins=logdaybins, label='All Issues')
plt.hist(lifetime[is_pr]/86400, bins=logdaybins, label='PRs')

plt.xscale('log')
plt.xlabel("Lifetime (days)")
plt.legend(loc='best')
plt.savefig("issue_lifetime_full.png")


plt.figure(2).clf()
plt.hist(lifetime/3600, bins=np.linspace(0,48,49), label='All Issues')
plt.hist(lifetime[is_pr]/3600, bins=np.linspace(0,48,49), label='PRs')
plt.xlabel("Lifetime (hours)")
plt.legend(loc='best')
plt.savefig("issue_lifetime_short.png")


lifetimes = []
for label in ProgressBar(unique_labels):
    mask = np.array([label in str(row['Labels']) for row in tbl], dtype='bool')
    lifetimes.append(lifetime[mask])

plt.figure(3).clf()
colors = plt.cm.spectral(np.linspace(0,1,len(unique_labels)))

plt.hist(lifetimes, bins=np.logspace(1, 8.25, 50), label=unique_labels, stacked=True, color=colors)
plt.xscale('log')

plt.xlabel("Lifetime (hours)")
plt.legend(bbox_to_anchor=(1, 1), loc='upper left', ncol=1)
plt.savefig("issue_lifetime_labeled.png", bbox_inches='tight')
