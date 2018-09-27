from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus
import config.config as config

app = Flask(__name__)
app.config.from_object(config.config)

db = SQLAlchemy(app)
from inhibition_bargraph.core.models import Experiment, Dataset

# Register blueprints
from inhibition_bargraph.views import home, api_blueprint
app.register_blueprint(home)
app.register_blueprint(api_blueprint, url_prefix='/api')

@app.errorhandler(Exception)
def internal_error(error):
    return render_template('error.html', error=error), 500
