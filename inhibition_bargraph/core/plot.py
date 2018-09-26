import inhibition_bargraph.api as api
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import operator
import io


plot_defaults = {
    'font.sans-serif': 'Arial',
    'font.family': 'sans-serif',
    'axes.labelsize': 11,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'legend.fontsize': 11,
    'legend.frameon': False,
}

errorbar_options = {
    'elinewidth': 1,
    'capsize': 1,
    'capthick': 0.5
}

BAR_WIDTH = 0.5


matplotlib.rcParams.update(plot_defaults)


class PlotData:
    def __init__(self, source_url, name, inverse):
        self.source_url = source_url
        self.name = name
        self.inverse = inverse
        self._data = self.init_data()

    @property
    def data(self):
        # slicing from one index because the first index is uniprot
        # zipping into three tuples containing list of symbols, ratios, stderrs
        return tuple(zip(*(r[1:] for r in sorted(list(self._data), key=operator.itemgetter(2)) if r[2] > 0)))

    def init_data(self):
        """Helper initialization method which creates experiment if needed."""
        experiment = api.get_experiment(self.source_url) or api.new_experiment(self.source_url, self.name)
        return api.get_dataset(experiment.experiment_id, self.inverse)

    def apply_whitelist(self, whitelist=None):
        if whitelist:
            self._data = (r for r in self._data if r[0] in whitelist)

    def apply_blacklist(self, blacklist=None):
        if blacklist:
            self._data = (r for r in self._data if r[0] not in blacklist)


def get_data_for_plot(source_url, name, inverse, whitelist=None, blacklist=None):
    all_data = PlotData(source_url, name, inverse)
    all_data.apply_whitelist(whitelist)
    all_data.apply_blacklist(blacklist)
    return all_data.data


def vertical_plot(name, symbols, ratios, stderrs):
    indices = np.arange(len(symbols))
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 4, forward=True)
    ax.bar(indices, ratios, BAR_WIDTH, yerr=stderrs, error_kw=errorbar_options, color='k', label=name)
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Ratio')
    ax.set_xticks(indices)
    ax.set_xticklabels(symbols, size=8, rotation='vertical')
    ax.legend(loc='upper left')
    plt.ylim(0, 2)
    plt.xlim(-1)
    plt.tight_layout()


def horizontal_plot(name, symbols, ratios, stderrs):
    indices = np.arange(len(symbols))
    fig, ax = plt.subplots()
    fig.set_size_inches(4, 8, forward=True)
    ax.barh(indices, ratios, BAR_WIDTH, xerr=stderrs, error_kw=errorbar_options, color='k', label=name)
    # add some text for labels, title and axes ticks
    ax.set_xlabel('Ratio')
    ax.set_yticks(indices)
    ax.set_yticklabels(symbols, size=8)
    ax.legend(loc='lower right')
    plt.xlim(0, 2)
    plt.ylim(-1)
    plt.tight_layout()

def plot(source_url, name, file_type, orientation, inverse=False, whitelist=None, blacklist=None):
    symbols, ratios, stderrs = get_data_for_plot(source_url, name, inverse, whitelist, blacklist)

    if orientation == 'vertical':
        vertical_plot(name, symbols, ratios, stderrs)
    else:
        horizontal_plot(name, symbols, ratios, stderrs)

    memory_file = io.BytesIO()
    plt.savefig(memory_file, format=file_type)
    memory_file.seek(0)
    return memory_file
