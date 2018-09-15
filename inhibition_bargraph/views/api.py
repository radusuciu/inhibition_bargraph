from flask import Blueprint, jsonify, send_file, request
from werkzeug import secure_filename
from http import HTTPStatus
from inhibition_bargraph.core.plot import plot_horizontal
import inhibition_bargraph.core.whitelist as whitelist
import inhibition_bargraph.core.blacklist as blacklist
import inhibition_bargraph.api as api


api_blueprint = Blueprint('api_blueprint', __name__)

@api_blueprint.route('/plot/<path:url>')
def generate_plot(url):
    name = request.args.get('name', url.split('/')[-2])

    memory_file = plot_horizontal(
        source_url=url,
        name=secure_filename(name),
        whitelist=whitelist.human_serine_hydrolases,
        blacklist=blacklist.human_serine_hydrolases
    )

    return send_file(
        memory_file,
        attachment_filename='{}.svg'.format(name)
    )


@api_blueprint.errorhandler(Exception)
def error_response(error):
    payload = 'error'
    return jsonify(payload), 500