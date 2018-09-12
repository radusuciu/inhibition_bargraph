from collections import defaultdict, namedtuple
from copy import deepcopy
import operator
import numpy as np
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import itertools
import numbers
import datetime
import requests
import pathlib
import numbers
import csv
import sys
import json

matplotlib.rcParams['font.sans-serif'] = "Arial"
matplotlib.rcParams['font.family'] = "sans-serif"


blacklist = [
    'P35030', 'P07477', 'P07478', # trypsins 
    'O15427', # SLC16A3
    'P00734', # F2
    'Q14703', # MBTSP1 (serine protease)
    'Q8NBP7', # PCSK9
]


def plot_horizontal(plot_name, datasets):
    data = format_data_for_plots(datasets)
    symbols = data.pop(0)

    N = len(symbols)

    ind = np.arange(N)
    height = 0.5 - (0.1 * len(datasets))

    fig, ax = plt.subplots()

    error_kw = {
        'elinewidth': 1,
        'capsize': 1,
        'capthick': 0.5
    }

    fig.set_size_inches(4, 8, forward=True)

    colors = ['k', 'r', 'c']

    def grouper(iterable, n, fillvalue=None):
        "Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return itertools.zip_longest(*args, fillvalue=fillvalue)

    for i, (ratios, stderr) in enumerate(grouper(data, 2)):
        pos = ind + (height + 0.1) * i
        label = '{} - {}'.format(datasets[i].inhibitor, datasets[i].concentration)
        ax.barh(pos, ratios, height, xerr=stderr, error_kw=error_kw, color=colors.pop(0), label=label)

    # add some text for labels, title and axes ticks
    ax.set_xlabel('Ratio')

    yticks = ind

    if len(datasets) == 1:
        yticks = yticks
    elif len(datasets) == 2:
        yticks = yticks + height/2 + 0.05
    elif len(datasets) == 3:
        yticks = yticks + height + 0.1

    ax.set_yticks(yticks)

    ax.tick_params(direction='out')
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_yticklabels(symbols, size=8)

    ax.legend(frameon=False, prop={'size': 11}, loc='lower right')

    plt.xlim(0, 2)
    plt.ylim(-1)
    plt.tight_layout()

    plt.savefig(str(DATA_OUTPUT_PATH.joinpath(plot_name)), format='svg')
