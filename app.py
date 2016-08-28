import ipdb
import os
from flask import Flask, jsonify, Response, request
from lxml import html
import requests
from testscrape import front_page_scraper, category_page_scraper
import json

app = Flask(__name__)

# call /list with example
# http://localhost:5000/list?city=sacramento&category=artists
@app.route("/list")
def list_Response():
    # city default if no request params
    city = "sfbay"
    if request.args.get('city'):
        city = request.args.get('city')
    fp = front_page_scraper(city)
    fp_listed = [{"title": k, "link": v, "api_query": (str(k).split(" ")[0])} for k, v in fp.category_dict.items()]

    if request.args.get('category'):
        cat = request.args.get('category')

        lookup_dict = dict((i['api_query'], i['link']) for i in fp_listed)
        category_url = lookup_cat(fp.category_dict.get(cat), lookup_dict.get(cat))

        if category_url != None:
            limit = request.args.get('limit')
            cs = category_page_scraper(category_url, cat, city, limit)
            cs.children()
            return Response(json.dumps(cs.children),  mimetype='application/json')
            # there was a category ^
    return Response(json.dumps(fp_listed),  mimetype='application/json')
    # there wasn't a category ^ scrape for a list of them



def lookup_cat(s1, s2):
    if s1 is None:
        return s2
    else:
        return s1

@app.route("/")
def root():
    return "hi, you're at the root of a super swell api!"

if __name__ == "__main__":
    app.run()
