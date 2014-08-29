"""
Makes some plots for commits and such

made gitlogstats file with:
git log --numstat --use-mailmap --format=format:"COMMIT,%H,%at,%aN"
"""

import numpy as np
from matplotlib import pyplot as plt

def parse_git_log(fn='gitlogstats', recentfirst=False, cumlines=False):
    """
    Returns (authors, datetimes, deltalines) arrays
    """
    from datetime import datetime

    authors = []
    deltalines = []
    datetimes = []

    with open(fn) as f:
        commitstrs = f.read().split('COMMIT,')[1:]

    for cs in commitstrs:
        lns = cs.strip().split('\n')
        chash, timestamp, author = lns.pop(0).split(',')
        timestamp = int(timestamp)

        authors.append(author)
        datetimes.append(datetime.utcfromtimestamp(timestamp))

        dellns = 0
        for l in lns:
            add, sub, filename = l.split('\t')
            dellns += int(add.replace('-', '0')) - int(sub.replace('-', '0'))
        deltalines.append(dellns)

    authors, datetimes, deltalines = [np.array(l) for l in (authors, datetimes, deltalines)]

    sorti = np.argsort(datetimes)
    revsorti = np.argsort(sorti)

    if cumlines:
        deltalines = np.cumsum(deltalines[sorti])[revsorti]

    if recentfirst:
        sorti = sorti[::-1]

    return tuple([a[sorti] for a in (authors, datetimes, deltalines)])


def loc_plot():
    from datetime import datetime

    authors, datetimes, nlines = parse_git_log(cumlines=True, recentfirst=False)

    plt.plot(datetimes, nlines, lw=2)

    yrlabels = [2011, 2012, 2013, 2014]

    plt.xticks([datetime(yr, 1, 1) for yr in yrlabels], yrlabels, fontsize=20)
    plt.ylabel('Lines of Code', fontsize=30)

    plt.tight_layout()


def commits_plot():
    from datetime import datetime

    authors, datetimes, deltalines = parse_git_log(recentfirst=False)

    plt.plot(datetimes, np.arange(len(datetimes)) + 1, lw=2)

    yrlabels = [2011, 2012, 2013, 2014]

    plt.xticks([datetime(yr, 1, 1) for yr in yrlabels], yrlabels, fontsize=20)
    plt.ylabel('Number of Commits', fontsize=30)

    plt.tight_layout()


def get_first_commit_map():
    authors, datetimes, deltalines = parse_git_log(recentfirst=False)

    firstcommit = {}
    for au, t in zip(authors, datetimes):
        if au not in firstcommit or firstcommit[au] > t:
            firstcommit[au] = t

    return firstcommit


def commiters_plot():
    from datetime import datetime

    firstcommit = get_first_commit_map()

    dts = np.sort(firstcommit.values())

    plt.plot(dts, np.arange(len(dts)) + 1, lw=2)

    yrlabels = [2011, 2012, 2013, 2014]

    plt.xticks([datetime(yr, 1, 1) for yr in yrlabels], yrlabels, fontsize=20)
    plt.ylabel('# of Code Contributors', fontsize=30)

    plt.tight_layout()


def site_visits_plot(fn='Analytics Astropy Audience Overview 20110101-20140101.csv'):
    from datetime import datetime
    from astropy.io import ascii

    d = ascii.read(fn)

    vs = np.array([v.replace(',', '') for v in d['Visits']], dtype=int)

    dts = []
    in2011 = []
    for dt in d['Day Index']:
        mon, day, yr = dt.split('/')
        in2011.append(yr == '11')
        dts.append(datetime(int('20' + yr), int(mon), int(day)))

    dts = np.array(dts)
    in2011 = np.array(in2011)

    plt.plot(dts[~in2011], vs[~in2011], lw=2)

    yrlabels = [2012, 2013, 2014]

    plt.xticks([datetime(yr, 1, 1) for yr in yrlabels], yrlabels, fontsize=20)
    plt.ylabel('Daily Web Page Visits', fontsize=30)

    plt.tight_layout()

    return dts, vs
