from flask import Blueprint, render_template, abort,  request, jsonify
from jinja2 import TemplateNotFound
from core.utils.loader import getFromKeyWords
from core.utils.parser import TimesNowScrapper
from datetime import datetime, timedelta
from core.utils.loader import *


home = Blueprint('home', __name__,template_folder='../../web/pages/home')

@home.route('/')
def index():
    # Im hoping I always find this
    return render_template('index.html')

@home.route('/parsing')
def index_copy():
    return render_template('index_copy.html')

@home.route('/fetch_news', methods=['POST'])
def fetch_news():
    start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%d')
    end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%d')
    print(f"GOT FETCH REQUEST with start {start_time} end : {end_time}")
    scraper = TimesNowScrapper(start_time, end_time)
    news_items = scraper.download_content()
    print(f"new_item size {len(news_items)}")
    return jsonify({'news' : news_items})  

@home.route('/get_news', methods=['POST'])
def get_news():
    start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%d')
    end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%d')
    print(f"GOT FETCH REQUEST with start {start_time} end : {end_time}")
    return jsonify({'news' : getNews(start_time, end_time)})

@home.route('/filter_news', methods=['POST'])
def filter_news():
    data = request.get_json()
    keywords = data.get('keywords', [])
    return jsonify({"news" : getFromKeyWords(keywords)})

@home.route('/latest')
def latest_news():
    today = datetime.now() - timedelta(days=1)
    yest = today - timedelta(days=2)
    news_items = getNews(yest, today)
    print(len(news_items))
    try:
        return render_template('latest.html', news_items=news_items)
    except TemplateNotFound :
        abort(400)
