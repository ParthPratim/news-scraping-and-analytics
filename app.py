from flask import Flask, render_template, abort,  request, jsonify
from jinja2 import TemplateNotFound
from core.utils.parser import TimesNowScrapper
from datetime import datetime, timedelta


app = Flask(__name__)

# news_data = [
#     {"title": "Breaking News 1", "content": "Content for news 1", "category": "World"},
#     {"title": "Breaking News 2", "content": "Content for news 2", "category": "Tech"},
# ]

@app.route('/')
def index():
    # Im hoping I always find this
    return render_template('index.html')

@app.route('/fetch_news', methods=['POST'])
def fetch_news():
    start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%d')
    end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%d')
    print(f"GOT FETCH REQUEST with start {start_time} end : {end_time}")
    scraper = TimesNowScrapper(start_time, end_time)
    news_items = scraper.download_content()
    print(f"new_item size {len(news_items)}")
    return jsonify({'news' : news_items})  

@app.route('/latest')
def latest_news():
    today = datetime.now()
    scraper = TimesNowScrapper(today, today)
    news_items = scraper.download_content()
    try:
        return render_template('latest.html', news_items=news_items)
    except TemplateNotFound :
        abort(400)

if __name__ == '__main__':
    app.run(debug=True)
