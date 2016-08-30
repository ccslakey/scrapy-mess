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
    city = one_or_another(request.args.get('city'), "sfbay")

    fp = front_page_scraper(city)

    if request.args.get('category'):
        cat = request.args.get('category')

        lookup_dict = dict((i['api_query'], i['link']) for i in fp.listed)
        category_url = one_or_another(fp.category_dict.get(cat), lookup_dict.get(cat))

        if category_url != None:
            limit = request.args.get('limit') or 100
            cs = category_page_scraper(category_url, cat, city, limit)
            cs.children()
            return Response(json.dumps(cs.children),  mimetype='application/json')
            # there was a category ^
    return Response(json.dumps(fp.listed),  mimetype='application/json')
    # there wasn't a category ^ scrape for a list of them


# softly return the category page url
def one_or_another(arg1, arg2):
    if arg1 is None:
        return arg2
    else:
        return arg1

@app.route("/")
def root():
    return "hi, you're at the root of a super swell api!"

if __name__ == "__main__":
    app.run()
