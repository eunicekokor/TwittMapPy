# import json
# import requests
# import tweepy
# import time
# from elasticsearch import Elasticsearch as es

# from tweepy.streaming import StreamListener
# from flask import Flask, render_template
# import certifi

# endpoint = 'tweetmap-env.bmcf8muqyd.us-west-2.elasticbeanstalk.com'

# es = es(host=endpoint,port=443, use_ssl=True, verify_certs=True, ca_certs=certifi.where())

# app=Flask(__name__)
# @app.route("/")
# def main():
#     return render_template('index.html')


# @app.route('/<key>')
# def search(key):
#     result = es.search(index='tweet',body={"query":{"match": {'text': key}}})
#     data = json.dumps(result);
#     return data

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask
from flask import render_template
from elasticsearch import Elasticsearch
import certifi
import json

# EB looks for an 'application' callable by default.
application = Flask(__name__)

endpoint = 'tweetmap-env.bmcf8muqyd.us-west-2.elasticbeanstalk.com'

es = Elasticsearch(host=endpoint,port=443, use_ssl=True, verify_certs=True, ca_certs=certifi.where())

@application.route('/')
def index():
    return render_template('index.html')


@application.route('/<keyword>')
def search(keyword):
    result = es.search(index='twittmap',body={"query":{"match": {'text': keyword}}})
    data = json.dumps(result);
    return data


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run(port=8081)
