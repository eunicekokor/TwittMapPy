from elasticsearch import Elasticsearch, RequestsHttpConnection
import tweepy
import json
import pprint
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys
from datetime import *
import time
import certifi
from requests_aws4auth import AWS4Auth
# from TwitterAPI import TwitterAPI
YOUR_ACCESS_KEY = "AKIAIFXS6NMDG6DNTGNQ"
YOUR_SECRET_KEY = "lwVBol6OuS32W4DA+kasw5Qv8W5HfrKFCMC9g01W"
REGION = "us-east-1"
global i

awsauth = AWS4Auth(YOUR_ACCESS_KEY, YOUR_SECRET_KEY, REGION, 'es')
host = "search-mytweetmap-zvx2ulax7nvfnzu2dmpixdybqu.us-east-1.es.amazonaws.com"
# es = Elasticsearch(
#     hosts=[{'host': host, 'port': 443}],
#     http_auth=awsauth,
#     use_ssl=True,
#     verify_certs=True,
#     connection_class=RequestsHttpConnection
# )
access_token="28203065-m0YfUbocnLSgTzmfV5kYX7FIhLHo71s9Pb36yu3jB"
access_token_secret="1xc2XNwgXhCEm34NbhDeuIEnPuDAqHkUrG2Wpp7W1p2ge"
consumer_key="euXCzLT4bHep6PMSwFha1X610"
consumer_secret="czLjLODWigoHvUxdXR7KhPoucrTP36HVxZtK19wqDATpQjM3tW"
es = Elasticsearch(
  hosts=[{
  'host': host,
  'port': 443,
}],
  http_auth=awsauth,
  use_ssl=True,
  connection_class=RequestsHttpConnection
  )
es.indices.create(index='test', ignore=400)

print (es.info())

class StdOutListener(StreamListener):
  def on_data(self, doc_data):
    json_data=json.loads(doc_data)
    # try:
    data={}
    # print(json_data)
    if json_data.get('coordinates') is not None:
      try:
        print ("got here2!!!")
        # print(json_data)
        data["coordinates"]= (json_data['coordinates']['coordinates'][0],json_data['coordinates']['coordinates'][1])
        data["name"]=json_data['user']['name']
        data["text"]=json_data['text']
        data["created_at"]=json_data['created_at']
        print ("printing data...\n")
        print (data)

        res = es.index(index="test", doc_type='tweet', body=str(data))

        print(res['created'])
        print ("hello world")
      except:
        pass
        # res2 = es.get(index="test", doc_type='tweet')
        # print ("printing {}".format("test"))
    elif json_data.get('place') is not None:
      try:
        print ("got here2!!!")
        # print(json_data)
        data["coordinates"]= (json_data['place']['bounding_box']['coordinates'][0][0][0],json_data['place']['bounding_box']['coordinates'][0][0][1])
        data["name"]=json_data['user']['name']
        data["text"]=json_data['text']
        data["created_at"]=json_data['created_at']
        print ("printing data...\n")
        print (data)

        res = es.index(index="test", doc_type='tweet', body=data)

        print(res['created'])
        print ("hello world")
      except:
        pass

    else:
        return

  def on_error(self, status):
      print (status)

def begin():
    i = 0

    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)
    stream.filter(track=['haiku', 'poem', 'poetry', 'obama', 'clinton', 'movie', 'review', 'food', 'film'])
begin()