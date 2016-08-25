import os
from flask import Flask, json
from lxml import html
import requests


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world"



@app.route("/hi")
def hi():
    return "hi"

if __name__ == "__main__":
    app.run()
