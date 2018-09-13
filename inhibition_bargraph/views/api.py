from flask import Blueprint, jsonify, send_file
from inhibition_bargraph.core.plot import plot_horizontal
import inhibition_bargraph.core.whitelist as whitelist
import inhibition_bargraph.core.blacklist as blacklist
import inhibition_bargraph.api as api


api_blueprint = Blueprint('api_blueprint', __name__,
                  template_folder='templates',
                  static_folder='static')

@api_blueprint.route('/')
def index():
    return jsonify('hello')

@api_blueprint.route('/plot/<path:url>')
def generate_plot(url):
    memory_file = plot_horizontal(
        source_url=url,
        name='wat',
        whitelist=whitelist.human_serine_hydrolases,
        blacklist=blacklist.human_serine_hydrolases
    )

    return send_file(
        memory_file,
        attachment_filename='wat.svg'
    )
