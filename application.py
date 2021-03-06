import json
import requests
import tweepy
import time
from elasticsearch import Elasticsearch, RequestsHttpConnection
from flask import Flask, render_template
import certifi
from requests_aws4auth import AWS4Auth

application = Flask(__name__)

YOUR_ACCESS_KEY = ""
YOUR_SECRET_KEY = ""
REGION = "us-east-1"
# host = 'tweetmap-env.bmcf8muqyd.us-west-2.elasticbeanstalk.com'
awsauth = AWS4Auth(YOUR_ACCESS_KEY, YOUR_SECRET_KEY, REGION, 'es')
host = 'search-mytweetmap-zvx2ulax7nvfnzu2dmpixdybqu.us-east-1.es.amazonaws.com'
# es = Elasticsearch([host])

# es = Elasticsearch(host=host,port=443,use_ssl=True,ca_certs=certifi.where(),verify_certs=True)
es = Elasticsearch(
  hosts=[{
    'host': host,
    'port': 443,
  }],
  http_auth=awsauth,
  use_ssl=True,
  verify_certs=True,
  connection_class=RequestsHttpConnection
  )

@application.route('/')
def index():
    return render_template('index.html')

# Whenever there is a request to this with a key, we get back results from elastic search
@application.route('/<key>')
def search(key):
    result = es.search(index='test',doc_type="tweet",body={
      "from":0,
      "size":100,
      "query":{
        "match": {
          'text': {
            "query":key,
            "operator":"and"
            }
          }
        }
      })
    # print (result)
    data = json.dumps(result['hits']['hits'])
    # for hit in result['hits']['hits']:
    #   print(hit)

    print ("length", len(result['hits']['hits']))
    return data


if __name__ == "__main__":
    application.debug = True
    application.run(port=8000)
