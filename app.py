import ipdb
import os
from flask import Flask, jsonify, Response, request
from lxml import html
import requests
from testscrape import front_page_scraper, category_page_scraper
import json

app = Flask(__name__)



@app.route("/categories")
def categories_Json_Response():
    # city default if no request params
    city = "sfbay"
    if request.args.get('city'):
        city = request.args.get('city')
    fp = front_page_scraper(city)


    if request.args.get('category'):
        cat = request.args.get('category')
        
        if fp.category_dict[cat] != None:
            cs = category_page_scraper(fp.category_dict[cat], cat ,city)
            # keys = [x for x in cs.category_dict.keys()]
            # vals = [x for x in cs.category_dict.values()]
            # ipdb.set_trace()

            return Response(json.dumps(cs.category_dict),  mimetype='application/json')
        return "hi"
        

    return Response(json.dumps(fp.category_dict),  mimetype='application/json')


@app.route("/")
def hi():
    return "hi"

if __name__ == "__main__":
    app.run()
