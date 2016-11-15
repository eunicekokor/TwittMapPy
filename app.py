import json
import requests
import tweepy
import time
from elasticsearch import Elasticsearch, RequestsHttpConnection
from flask import Flask, render_template
import certifi
from requests_aws4auth import AWS4Auth

app = Flask(__name__)

YOUR_ACCESS_KEY = "AKIAIFXS6NMDG6DNTGNQ"
YOUR_SECRET_KEY = "lwVBol6OuS32W4DA+kasw5Qv8W5HfrKFCMC9g01W"
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

@app.route('/')
def index():
    return """ <!DOCTYPE html>
<html>
  <head>
    <style>
       #map {
        height: 100vh;
        width: 100vw;
        left: 0;
       }
    </style>
  </head>
  <body>
    <h3>Tweet Map App</h3>
    <select id="drop">
      <option value="obama">obama</option>
      <option  value="trump">trump</option>
      <option value="clinton">clinton</option>
    </select>
    <div id="map"></div>
    <script>
    var map;
      function initMap() {
        var columbia = {lat: 40.8075, lng: -73.9626};
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 5,
          center: columbia
        });
        var marker = new google.maps.Marker({
          position: columbia,
          map: map
        });

        document.getElementById("query").onchange = function(){
          keyword = this.value;
          reQuery(keyword);
        }

      }
      function reQuery(param){


        console.log(this.responseText);
        // var search_str = "haiku";
        var oReq = new XMLHttpRequest();
        oReq.addEventListener("load", reqListener);
      // var url = "http://localhost:3000/tweets/getTweets?search="+search_str;
      // console.log(url);
      oReq.open("GET", "/" + param);
      oReq.send();
      }

    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyACGeO9TeMbOLSk1We5O5Yrh5FXnGUQSbs&callback=initMap">
    </script>
  </body>
</html>


    <script>
      var map;
      var infowindow;
      var markers = [];
      var keyword;
      function initMap() {
        var center = {lat: 0, lng: 0};
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 2,
          center: center
        });
        document.getElementById("drop").onchange = function(){
          keyword = this.value;
          start(keyword);
        }
        setInterval(function(){start(keyword)},10000);
      }
      function addContent(tweets){
          var myPosition = {lat: tweets.geo[1], lng: tweets.geo[0] };
          var time = tweets.time;
          var user = tweets.user;
          var text = tweets.text;
          var prev_infowindow = false;
          // API Reference: https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple
          var marker = new google.maps.Marker({
              position:myPosition,
              map: map
          });
          markers.push(marker);
          setMapOnAll(map);
          google.maps.event.addListener(marker, "click", function () {
                if (infowindow) {infowindow.close();}
                var contentString =  '<div id="content">'+'<div id="siteNotice">'+'</div>'+
                          '<h1 id="firstHeading" class="Twitter message">Twitter message</h1>'+
                          '<div id="bodyContent">' + user + ' : '  +  text +'</div>'+'</div>';
                infowindow = new google.maps.InfoWindow({
                  content: contentString
                });
                infowindow.open(map, marker);
          });
      }
      function start(keyword) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
          if (this.readyState == 4 && this.status == 200) {
            deleteMarkers();
            var obj = JSON.parse(this.responseText);
            var tweets = obj.hits.hits
            for(var i = 0; i < tweets.length; i++){
                addContent(tweets[i]._source)
            }
          }
        };
        xhttp.open("GET", "/" + keyword, true);
        xhttp.send();
      }
      function deleteMarkers() {
        setMapOnAll(null);
        markers = [];
      }
      function setMapOnAll(map) {
        for (var i = 0; i < markers.length; i++) {
          markers[i].setMap(map);
        }
      }
    </script>

"""
    # return render_template('index.html')


@app.route('/<key>')
def search(key):
    result = es.search(index='test',doc_type="tweet",body={"query":{"match": {'text': key}}})
    print (result)
    data = json.dumps(result)
    for hit in result['hits']['hits']:
      print(hit)
    # print (data.hits.hits)
    print ("test")
    return data


if __name__ == "__main__":
    app.debug = True
    app.run(port=8000)
