from inhibition_bargraph.core.models import Experiment, Dataset
from inhibition_bargraph.core import get_dataset_from_url
from inhibition_bargraph import db


def get_experiment(source_url):
    return Experiment.query.filter_by(source_url=source_url).first()
    
def get_dataset(experiment_id):
    return db.session.query(
        Dataset.uniprot, Dataset.symbol, Dataset.median, Dataset.stdev
    ).filter_by(dataset_id=experiment_id).all()

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
