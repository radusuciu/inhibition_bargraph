from flask import Blueprint, jsonify
import inhibition_bargraph.api as api


api_blueprint = Blueprint('api_blueprint', __name__,
                  template_folder='templates',
                  static_folder='static')

@api_blueprint.route('/')
def index():
    return jsonify('hello')
