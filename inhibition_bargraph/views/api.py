from flask import Blueprint, jsonify, send_file, request
from werkzeug import secure_filename
from http import HTTPStatus
from inhibition_bargraph.core.plot import plot
from inhibition_bargraph.core.exceptions import DatasetNotFound
from sqlalchemy.exc import DBAPIError
import inhibition_bargraph.core.whitelist as whitelist
import inhibition_bargraph.core.blacklist as blacklist
import inhibition_bargraph.api as api


api_blueprint = Blueprint('api_blueprint', __name__)

@api_blueprint.route('/plot/<path:url>')
def generate_plot(url):
    name = request.args.get('name', url.split('/')[-2])

    file_type = request.args.get('type')
    file_type = file_type if file_type in ('png', 'svg') else 'svg'

    memory_file = plot_horizontal(
        source_url=url,
        name=secure_filename(name),
        file_type=file_type,
        whitelist=whitelist.human_serine_hydrolases,
        blacklist=blacklist.human_serine_hydrolases
    )

    return send_file(
        memory_file,
        attachment_filename='{}.{}'.format(name, file_type),
    )


@api_blueprint.errorhandler(DBAPIError)
def error_response(error):
    payload = 'error'
    api.db.session.rollback()
    return jsonify(payload), 500

@api_blueprint.errorhandler(DatasetNotFound)
def dataset_not_found(error):
    payload = 'dataset not found'
    return jsonify(payload), 404
