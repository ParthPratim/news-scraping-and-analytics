from flask import current_app as app
from flask import jsonify
from datetime import datetime
from bson.json_util import dumps

def getNews(start_time : datetime , end_time : datetime) :
    db = app.db

    print(f"Now getting news from {start_time} to {end_time}")
    news_list = db.toi_collection.find({
        "published_date": {
            "$gte" : start_time,
            "$lte" : end_time
        }
    }
    )
    news_list = list(news_list)
    result_list = []
    for news in news_list:
        news["_id"] = str(news["_id"])
        result_list.append(news.copy())
        
    return news_list

