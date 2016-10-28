# import tweepy
# from tweepy.streaming import StreamListener
# import json
# from elasticsearch import Elasticsearch
# import time
# from tweepy import OAuthHandler
# from tweepy import Stream, API
# from flask import Flask, render_template
# from TwitterAPI import TwitterAPI
# import googlemaps

# consumer_key= "euXCzLT4bHep6PMSwFha1X610"
# consumer_secret= "czLjLODWigoHvUxdXR7KhPoucrTP36HVxZtK19wqDATpQjM3tW"
# access_token= "28203065-m0YfUbocnLSgTzmfV5kYX7FIhLHo71s9Pb36yu3jB"
# access_token_secret= "1xc2XNwgXhCEm34NbhDeuIEnPuDAqHkUrG2Wpp7W1p2ge"
# es = Elasticsearch([{'host': 'http://tweetmap-env.bmcf8muqyd.us-west-2.elasticbeanstalk.com/', 'port': 443}])

# gmaps = googlemaps.Client(key='AIzaSyACGeO9TeMbOLSk1We5O5Yrh5FXnGUQSbs')


# class TweetPyListener(StreamListener):
#     def on_data(self, data):
#             tweet = json.loads(data)
#             if tweet['lang'] == 'en' and tweet['user'].get('location') is not None:
#               location = tweet['user'].get('location')
#               tweet_id = str(tweet['id'])
#               geocode_result = gmaps.geocode(location)
#               raw_tweet = {
#                   'user': tweet['user']['screen_name'],
#                   'text': tweet['text'],
#                   'location': tweet['user']['location'],
#                   'coordinates': geocode_result,
#                   'time': tweet['created_at']
#               }
#               es.index(index='tweets', id=tweet_id, body=raw_tweet)


#     def on_error(self, status):
#         print(status)
#         if str(status) == '420':
#             print "Sleeping 3 sec"
#             time.sleep(30)
#         return

# if __name__ == "__main__":
#     auth = OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_token_secret)

#     es = Elasticsearch(hosts=['http://tweetmap-env.bmcf8muqyd.us-west-2.elasticbeanstalk.com/'])
#     # es.indices.create(index='twitter',ignore = 400)
#     l = TweetPyListener()
#     stream = Stream(auth, l)

#             # stream.filter(track=['haiku', 'poem', 'poetry'])

#     while True:
#        stream.filter(track=['sports', 'music', 'hillary'])

import json
from elasticsearch import Elasticsearch as es
import tweepy
import pprint
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys
import datetime
import time
from TwitterAPI import TwitterAPI

access_token="28203065-m0YfUbocnLSgTzmfV5kYX7FIhLHo71s9Pb36yu3jB"
access_token_secret="1xc2XNwgXhCEm34NbhDeuIEnPuDAqHkUrG2Wpp7W1p2ge"
consumer_key="euXCzLT4bHep6PMSwFha1X610"
consumer_secret="czLjLODWigoHvUxdXR7KhPoucrTP36HVxZtK19wqDATpQjM3tW"

class StdOutListener(StreamListener):

  def on_data(self, doc_data):
      print (doc_data)
      json_data=json.loads(doc_data)
      try:
          data={}
          if json_data['coordinates'] is not None:
              data["lat"]=json_data['coordinates']['coordinates'][0]
              data["longtitude"]=longtitude=json_data['coordinates']['coordinates'][1]
          elif json_data['place'] is not None:
              data["lat"]=json_data['place']['bounding_box']['coordinates'][0][0][0]
              data["longtitude"]=json_data['place']['bounding_box']['coordinates'][0][0][1]
          else:
              return
          data["text"]=json_data['text']
          data["name"]=json_data['user']['name']
          data["created_at"]=json_data['created_at']
          print data
          res=es.index(index="tweet", doc_type='tweet', body=data)
          print (res['created'])
      except:
          return

  def on_error(self, status):
      print status

if __name__ == "__main__":
    while True:
        try:
            l = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            stream = Stream(auth, l)
            stream.filter(track=['haiku', 'poem', 'poetry', 'obama', 'clinton'])

        except:
            continue
