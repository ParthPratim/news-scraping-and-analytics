from flask import Blueprint

stats_api = Blueprint('stats', __name__)

@stats_api.route('/hello')
def hello():
    return "hello world"