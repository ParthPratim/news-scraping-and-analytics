from flask import Blueprint, render_template, current_app, jsonify, request
import json
import pandas as pd
import random
from collections import defaultdict
import os
import operator
from flask import current_app as app


stats_api = Blueprint('stats', __name__,template_folder='../../web/pages/stats-api')

def get_keywords_list(coll, year=True):
    return [ f['tag'] for f in list(coll.find({
        "year" : year,
        "filter" : 2,
    }, {
        "_id" : 0,
        "tag" : 1
    }))]

def process(data, year):
    if year:
        pot_labels = range(2002,2025,1)
    else:
        pot_labels = range(1,13,1)
    data = list(data)
    
    s_data = defaultdict(lambda: 0)
    
    for d in data:
        for p in pot_labels:
            if str(p) in d:
                s_data[str(p)] += d[str(p)]
    l = list(s_data.keys())
    v = list(s_data.values())
    if len(l) > 1 and l[0] > l[1]:
        l.reverse() 
        v.reverse()
    
    return {
        "labels" : l,
        "values" : v
    }

def get_temporal_data(coll, keywords = [], sources = None, year = True):
    

    if keywords == [] and sources == None:
        # find cumulative
        return process(coll.find({
            "year" : year,
            "filter" : 1
        }), year)
    else:
        kw1 = defaultdict(lambda: [])

        kw2 = defaultdict(lambda: [])
        
        if keywords != []:
            kw1 = process(coll.find({
                "year" : year,
                "filter" : 2,
                "tag" : {
                    "$in" : keywords
                }
            }),year)
        
        if sources:
            kw2 = process(coll.find({
                "year" : year,
                "filter" : 3,
                "tag" : sources
            }),year)
        
        combined = defaultdict(lambda : 0)
        for j in range(len(kw1['labels'])):
            combined[kw1['labels'][j]] = kw1['values'][j]

        for j in range(len(kw2['labels'])):
            combined[kw2['labels'][j]] = min(combined[kw2['labels'][j]], kw2['values'][j])
        
        l = list(combined.keys())
        v = list(combined.values())
        if len(l) > 1 and l[0] > l[1]:
            l.reverse() 
            v.reverse()
        return {
            "labels" : l,
            "values" : v
        }
             

def getkwshare(year):
    doc = app.db.statistics.find_one({
        "year" : True,
        "filter" : 5,
        "tag" : year
    },{
        "_id" : 0,
        "year" : 0,
        "filter" : 0,
        "tag" : 0
    })

    
    s_doc = sorted(doc.items(), key=operator.itemgetter(1), reverse=True)

    k = min(5 , len(s_doc))
    
    prep = [ b for a,b in  s_doc[:k]]

    return [a for a,b in s_doc[:k] ] , prep

            
@stats_api.route('/vizmaster')
def stats_home():

    db = app.db

    context = {
    }

    all_articles = db.statistics.find_one({
        "year" : True,
        "filter" : 1
    })
    
    context['total_articles'] = sum([ all_articles[t] for t in all_articles.keys() if t not in ['_id', "year", "filter"]])
    context['mrange'] = min([t for t in all_articles.keys() if t not in ['_id', "year", "filter"]]) + " - 2024" ;
    context['num_keywords'] = db.statistics.count_documents({
        "year" : True,
        "filter" : 2
    })
    context['sources'] = 1

    d1 = get_temporal_data(db.statistics)
    context['labels1'] = list(d1['labels'])
    context['data1'] = list(d1['values'])
    context['keyword_list'] = list(get_keywords_list(db.statistics))

    d2 = get_temporal_data(db.statistics, keywords=["BJP"])
    
    context['labels2'] = list(d2['labels'])
    context['data2'] = list(d2['values'])

    d3 = process(db.statistics.find({
        "year" : True,
        "filter" : 4
    }),True)

    context['labels3'] = list(d3['labels'])
    context['data3'] = list(d3['values'])   

    a,b  = getkwshare(2024)
    context['top5_labels'] = a
    context['top5_values'] = b

    return render_template("viz1.html", **context)

@stats_api.route('/api/plot2/<keyword>/<unit>', methods=['GET'])
def get_keyword_timeline(keyword,unit):
    
    db = app.db

    
    d1 = get_temporal_data(db.statistics, keywords=[keyword])
    
    return jsonify({
        "labels" : list(d1['labels']),
        "data" : list(d1['values']),
    })


@stats_api.route('/api/plot6/<year>', methods=['GET'])
def get_kw_year_share(year):
    

    a,b  = getkwshare(int(year))
    
    return jsonify({
        "labels" : a,
        "data" : b,
    })



@stats_api.route('/api/get-keyword-comparison', methods=['POST'])
def get_keyword_comparison():
    db = app.db
    req_data = request.json

    kw1 = req_data['keyword1'] 
    kw2 = req_data['keyword2'] 
    unit = req_data['unit']

    year = False
    if unit == "year":
        year = True

    d1 = get_temporal_data(db.statistics, keywords=[kw1], year=year)
    d2 = get_temporal_data(db.statistics, keywords=[kw2], year=year)

    x = list(set(list(d1['labels']) + list(d2['labels'])))
    if len(x) > 1 and x[0] > x[1]:
        x.reverse()

    return jsonify({
        "labels" : x,
        "data1" : list(d1['values']),
        "data2" : list(d2['values']),
    })

@stats_api.route('/viewer/<keyword>', methods=['GET'])
def stats_viewer(keyword):
    db = app.db
    d1 = get_temporal_data(db.statistics, keywords=[keyword])
    context = {
        "keyword" : keyword,
        "labels" : list(d1['labels']),
        "values" : list(d1['values'])
    }
    return render_template("viewer.html", **context)