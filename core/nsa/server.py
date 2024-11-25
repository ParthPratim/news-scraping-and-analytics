from flask import Flask
from flask_pymongo import PyMongo
from core.stats import *
from core.utils import *
from core.config import ApplicationConfig
import json

def setup_mongo_db_documents(app):
    app.config["MONGO_URI"] = "mongodb://root:root@mongo:27017/news_db?authSource=admin"
    mongo = PyMongo(app)
    app.db = mongo.db

    # Statistics 
    def create_if_not_exists(doc_name):
        doc = app.db.statistics.find_one({
            "_id" : doc_name
        })
        
        if not doc:
            app.db.statistics.insert_one({
                "_id" : doc_name
            })
    
    return 
    


# https://flask.palletsprojects.com/en/stable/tutorial/factory/
def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True, static_folder='../../web/static/scripts/')
    app.config.from_object(ApplicationConfig)
    app.register_blueprint(stats_api, url_prefix='/stats')
    app.register_blueprint(home)
    setup_mongo_db_documents(app)
    
    return app
    


