from inhibition_bargraph.core.models import Experiment, Dataset
from inhibition_bargraph.core import get_dataset_from_url
from inhibition_bargraph import db
import itertools
import statistics
import operator
import math


def get_experiment(source_url):
    return Experiment.query.filter_by(source_url=source_url).first()
    
def get_dataset(experiment_id, inverse=True):
    flat_dataset = db.session.query(
        Dataset.uniprot, Dataset.symbol, Dataset.ratio
    ).filter_by(dataset_id=experiment_id).order_by(Dataset.uniprot).all()
    aggregate_dataset = []
    for uniprot, g in itertools.groupby(flat_dataset, operator.itemgetter(0)):
        items = list(g)
        ratios = [float(i[2]) for i in items if i[2]]
        if inverse:
            ratios = [1/r for r in ratios]
        median = statistics.median(ratios) if ratios else 0
        stderr = statistics.stdev(ratios)/math.sqrt(len(ratios)) if len(ratios) > 1 else 0
        aggregate_dataset.append((
            uniprot, items[0][1], median, stderr
        ))
    return aggregate_dataset

def new_experiment(url, name):
    experiment = Experiment(source_url=url, name=name)
    db.session.add(experiment)
    # flush so we can get id
    db.session.flush()
    headers, rows = get_dataset_from_url(url)
    db.session.add_all(
        Dataset(dataset_id=experiment.experiment_id, **dict(zip(headers, row)))
        for row in rows
    )
    db.session.commit()
    return experiment
