import json
import requests
import tweepy
import time
from elasticsearch import Elasticsearch
from flask import Flask, render_template
import certifi

app = Flask(__name__)

host = 'tweetmap-env.bmcf8muqyd.us-west-2.elasticbeanstalk.com'
es = Elasticsearch(host=host,port=443,use_ssl=True,ca_certs=certifi.where(),verify_certs=True)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<key>')
def search(keyword):
    result = es.search(index='tweet',body={"query":{"match": {'text': keyword}}})
    data = json.dumps(result);
    return data


if __name__ == "__main__":
    app.debug = True
    app.run(port=8000)
