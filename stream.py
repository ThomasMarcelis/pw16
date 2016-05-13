import sqlite3
import time
import queue
from flask import Flask, Response, redirect, request, url_for
import urllib
import requests
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


#consumer key, consumer secret, access token, access secret.

app = Flask(__name__)

@app.route('/')
def index():

    if request.headers.get('accept') == 'text/event-stream':

        def events():
            print('in events')
            id = 0
            conn = sqlite3.connect('tweets.db')
            c = conn.cursor()
            lasttweet = None;
            while True:
                time.sleep(1)
                c.execute('SELECT * FROM tweets ORDER BY date DESC LIMIT 10')
                tweet = c.fetchone()
                if not tweet[1] == lasttweet:
                    lasttweet = tweet[1]
                    id += 1;
                    yield 'id:' + str(id) + '\ndata:<span class="' + tweet[0] + '">' + urllib.parse.unquote(tweet[1]) + '</span>\n\n'
            conn.close()
        return Response(events(), mimetype='text/event-stream')
    return redirect(url_for('static', filename='index.html'))

if __name__ == "__main__":
    app.run(host='localhost', port=23423)



