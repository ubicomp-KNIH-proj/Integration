from flask import Blueprint, render_template
from pymongo import MongoClient

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def hello_flsk():
    return 'Main page!'
    
@bp.route('/hello')
def index():
    return 'Flask index'

@bp.route('/mongo')
def mongoT():
    client = MongoClient('localhost', 27017)
    db = client['test']
    col = db["mongot"]
    
    results = col.find()
    # client.close()
    return render_template('mongo.html', data=results)

