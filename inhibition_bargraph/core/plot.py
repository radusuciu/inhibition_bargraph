import inhibition_bargraph.api as api
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import operator
import io


plot_defaults = {
    'font.sans-serif': 'Arial',
    'font.family': 'sans-serif'
}

matplotlib.rcParams.update(plot_defaults)


class PlotData:
    def __init__(self, source_url, name):
        self.source_url = source_url
        self.name = name
        self._data = self.init_data()

    @property
    def data(self):
        # slicing from one index because the first index is uniprot
        # zipping into three tuples containing list of symbols, ratios, stderrs
        return tuple(zip(*(r[1:] for r in sorted(list(self._data), key=operator.itemgetter(2)) if r[2] > 0)))

    def init_data(self):
        """Helper initialization method which creates experiment if needed."""
        experiment = api.get_experiment(self.source_url) or api.new_experiment(self.source_url, self.name)
        return api.get_dataset(experiment.experiment_id)

    def apply_whitelist(self, whitelist=None):
        if whitelist:
            self._data = (r for r in self._data if r[0] in whitelist)

    def apply_blacklist(self, blacklist=None):
        if blacklist:
            self._data = (r for r in self._data if r[0] not in blacklist)


def plot_horizontal(source_url, name, file_type, whitelist=None, blacklist=None):
    all_data = PlotData(source_url, name)
    all_data.apply_whitelist(whitelist)
    all_data.apply_blacklist(blacklist)
    symbols, ratios, stderrs = all_data.data

    N = len(symbols)

    indices = np.arange(N)
    height = 0.4

    fig, ax = plt.subplots()
    fig.set_size_inches(4, 8, forward=True)

    error_kw = {
        'elinewidth': 1,
        'capsize': 1,
        'capthick': 0.5
    }

    ax.barh(indices, ratios, height, xerr=stderrs, error_kw=error_kw, color='k', label=name)

    # add some text for labels, title and axes ticks
    ax.set_xlabel('Ratio')

    ax.set_yticks(indices)
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

    memory_file = io.BytesIO()
    plt.savefig(memory_file, format=file_type)
    memory_file.seek(0)
    return memory_file
