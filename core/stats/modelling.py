from collections import defaultdict

"""
Optimization:
----------------
Maintain a document which stores a map of datetimes of integers
After every scrap update this document store to increment the datetime 
based on which date was the news article published 

"""

def update_news_publishing_trends(news_list):
    update_successful = True
    # Todo 1. Load MongoDB object, and update date_map[news['publish_date']] += 1

    return update_successful

def get_news_publishing_trends():

    news_map = defaultdict(lambda : x)

    # Todo 1. Open MongoDB object, and return back the current statistics
    
    """
    { 'month-year' : 'number-of-articles-published-on-this-month-year' }
    """
    
    return news_map
