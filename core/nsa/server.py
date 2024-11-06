from flask import Flask
from core.stats import *
from core.utils import *
from core.config import ApplicationConfig
import json

# https://flask.palletsprojects.com/en/stable/tutorial/factory/
def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True, static_folder='../../web/static/scripts/')
    app.config.from_object(ApplicationConfig)
    app.register_blueprint(stats_api, url_prefix='/stats')
    app.register_blueprint(home)
    
    return app
    


