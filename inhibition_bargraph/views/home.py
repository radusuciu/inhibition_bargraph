from flask import Blueprint, render_template
from flask import request
from inhibition_bargraph import db

home = Blueprint('home', __name__,
    template_folder='templates',
    static_folder='static'
)


@home.route('/')
def index():
    plot_href = None

    if request.args.get('source_url'):
        keys_to_pass = ('type', 'name', 'inverse', 'orientation')
        args_to_pass = '&'.join([ '{}={}'.format(a, request.args.get(a)) for a in keys_to_pass if request.args.get(a) ])
        plot_href = '/api/plot/{}?{}'.format(request.args.get('source_url'), args_to_pass)
        print(plot_href)

    return render_template('index.html', plot_href=plot_href)

@home.before_app_first_request
def create_db():
    db.create_all()
    db.session.commit()
