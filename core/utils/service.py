from flask import Blueprint, render_template, abort,  request, jsonify
from jinja2 import TemplateNotFound
from core.utils.parser import TimesNowScrapper
from datetime import datetime, timedelta


home = Blueprint('home', __name__,template_folder='../../web/pages/home')

@home.route('/')
def index():
    # Im hoping I always find this
    return render_template('index.html')

@home.route('/fetch_news', methods=['POST'])
def fetch_news():
    start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%d')
    end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%d')
    print(f"GOT FETCH REQUEST with start {start_time} end : {end_time}")
    scraper = TimesNowScrapper(start_time, end_time)
    news_items = scraper.download_content()
    print(f"new_item size {len(news_items)}")
    return jsonify({'news' : news_items})  

@home.route('/latest')
def latest_news():
    today = datetime.now()
    scraper = TimesNowScrapper(today, today)
    news_items = scraper.download_content()
    try:
        return render_template('latest.html', news_items=news_items)
    except TemplateNotFound :
        abort(400)
