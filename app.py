import json
import requests
import tweepy
import time
from elasticsearch import Elasticsearch as es

from tweepy.streaming import StreamListener
from flask import Flask, render_template


app=Flask(__name__)
@app.route("/")
def main():
    return render_template('index.html')


@app.route('/<key>')
def search(keyword):
    result = es.search(index='tweet',body={"query":{"match": {'text': key}}})
    data = json.dumps(result);
    return data

if __name__ == "__main__":
    app.run(debug=True)
