"""Le models."""
from inhibition_bargraph import db
from sqlalchemy import func

Column = db.Column
Text = db.Text
Integer = db.Integer
Numeric = db.Numeric


class Experiment(db.Model):
    """Holds experimental metadata."""
    __tablename__ = 'experiment'
    experiment_id = Column(Integer, primary_key=True)

    name = Column(Text, index=True)
    source_url = Column(Text, index=True, unique=True)
    # creation date
    date = Column(db.DateTime, server_default=func.now())


class Dataset(db.Model):
    """Holds actual experimental data."""
    __tablename__ = 'dataset'
    entry_id = Column(Integer, primary_key=True)
    
    dataset_id = Column(db.Integer, db.ForeignKey('experiment.experiment_id'), index=True)
    uniprot = Column(Text, index=True)
    description = Column(Text)
    symbol = Column(Text, index=True)
    median = Column(Numeric)
    stdev = Column(Numeric)
