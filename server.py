import tweepy
from tweepy.streaming import StreamListener
import json
from elasticsearch import Elasticsearch
import time
from tweepy import OAuthHandler
from tweepy import Stream
from flask import Flask, render_template
from TwitterAPI import TwitterAPI


consumer_key= "euXCzLT4bHep6PMSwFha1X610"
consumer_secret= "czLjLODWigoHvUxdXR7KhPoucrTP36HVxZtK19wqDATpQjM3tW"
access_token= "28203065-m0YfUbocnLSgTzmfV5kYX7FIhLHo71s9Pb36yu3jB"
access_token_secret= "1xc2XNwgXhCEm34NbhDeuIEnPuDAqHkUrG2Wpp7W1p2ge"
api = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

class TweetPyListener(StreamListener):
    def on_data(self, data):
        if data:
            # print data
            jsonData = json.loads(data)
            if jsonData['place'] is not None:
                es.index(index='twitter',doc_type='tweet',body=jsonData)
                print jsonData
                return True
            if jsonData['coordinates'] is not None:
                es.index(index='twitter',doc_type='tweet',body=jsonData)
                print jsonData
                return True



    def on_error(self, status):
        print(status)
        if status == 420:
            print "Sleeping 3 sec"
            time.sleep(30)
        return

    def on_exception(self, exception):
        """Called when an unhandled exception occurs."""
        time.sleep(30)
        return


if __name__ == "__main__":
    es = Elasticsearch(hosts=['http://tweetmap-env.bmcf8muqyd.us-west-2.elasticbeanstalk.com/'])
    # es.indices.create(index='twitter',ignore = 400)
    l = TweetPyListener()

    # auth = OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    print "WHY"
    while True:
      try:
        # stream = Stream(auth, l)
        api.filter(track=['election', 'polls', '538','government', 'us', 'america', 'vote', 'ballot', 'trump', 'clinton'])
        # r = api.request('statuses/filter', {'track':'election,polls,538,government,us,america,vote,ballot,trump,clinton'})
        # for item in r:
        # print(item)
      except Exception as e:
        pass
