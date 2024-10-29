from flask import Blueprint, render_template, current_app
import json
import pandas as pd
from collections import defaultdict
from datetime import datetime
import os

stats_api = Blueprint('stats', __name__,template_folder='../../web/pages/stats-api')

@stats_api.route('/vizmaster')
def stats_home():
    data_file = current_app.config['SAMPLE_TEST_DATA_PATH']
    with open(data_file , 'r') as f:
        data = json.load(f)
    
    date_count = defaultdict(lambda : 0)
    kw_count = defaultdict(lambda : 0)
    src_count = defaultdict(lambda : 0)

    for sample in data:
        date_count[sample['posted_date']] += 1
        for kw in sample['keywords']:
            kw_count[kw]+=1
        src_count[sample['source']] += 1
    
    kw_count = dict(sorted(kw_count.items(), key=lambda x: x[1])[:20])
    
    context = {
        'labels' : list(date_count.keys()),
        'data' : list(date_count.values()),
        'kw_labels' : list(kw_count.keys()),
        'kw_data' : list(kw_count.values()),
        'src_labels' : list(src_count.keys()),
        'src_data' : list(src_count.values()),
    }

    return render_template("viz1.html", **context)
