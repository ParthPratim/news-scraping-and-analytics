from flask import Flask, render_template, abort
from jinja2 import TemplateNotFound

app = Flask(__name__)

news_data = [
    {"title": "Breaking News 1", "content": "Content for news 1", "category": "World"},
    {"title": "Breaking News 2", "content": "Content for news 2", "category": "Tech"},
]

@app.route('/')
def news_feed():
    try :
        return render_template('news_feed.html', news=news_data)
    except TemplateNotFound:
        abort(404)

if __name__ == '__main__':
    app.run()
