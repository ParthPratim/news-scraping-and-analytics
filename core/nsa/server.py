from flask import Flask
from core.stats.api import *

# https://flask.palletsprojects.com/en/stable/tutorial/factory/
def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    
    app.register_blueprint(stats_api, url_prefix='/stats')
    app.add_url_rule('/', endpoint='index')
    
    return app
    


