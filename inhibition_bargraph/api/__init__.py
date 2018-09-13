from inhibition_bargraph.core.models import Experiment, Dataset
from inhibition_bargraph.core.parse import get_dataset_from_url


def new_experiment(url, name):
    db.session.add(Experiment(source_url=url, name=name))

