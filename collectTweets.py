import time
import sqlite3
import urllib
import requests
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

ckey="nFxoqlFG5ilCPwj3EXq4sAzG1"
csecret="f8Si1Ixzwfy8Di7TSOvvLQhxExacEhvL607ouDIKAVcXOQj4kQ"
atoken="15661639-GVXAVX3ms3tMJXsADhIpJtCu5B0dbFYDT290EHhTE"
asecret="VNtuxQGZFyLn9BSY7EbsrR4928C5zGWiKTn9Gn4PIO1dC"



def getEmotion(text):
    url = 'https://4c6eefca-464f-4bc2-b505-f17cfa5f2b9d:22GgfkHwjOsu@gateway.watsonplatform.net/tone-analyzer-beta/api/v3/tone?version=2016-02-11&text='
    encodedtext = urllib.parse.quote(text)
    requestUrl = url + encodedtext
    emotions = requests.get(requestUrl)
    emotions = emotions.json()
    return selectEmotion(emotions)

def selectEmotion(emotions):
    for category in emotions.get('document_tone').get('tone_categories'):
        if category.get('category_id') == 'emotion_tone':
            score = 0
            emotion = ''
            for tone in category.get('tones'):
                if tone.get('score') > score:
                    score = tone.get('score')
                    emotion = tone.get('tone_name')
            return emotion
    return 'emotionless'

class listener(StreamListener):

    def on_data(self, data):
        jason = json.loads(data)

        conn = sqlite3.connect('tweets.db')
        c = conn.cursor()
        print("INSERT INTO tweets VALUES ('" + getEmotion(jason.get('text')) + "','" + urllib.parse.quote(jason.get('text')) + "','" + str(time.time()) + "')")
        c.execute("INSERT INTO tweets VALUES ('" + getEmotion(jason.get('text')) + "','" + urllib.parse.quote(jason.get('text')) + "','" + str(time.time()) + "')")
        conn.commit()
        conn.close()

        print(getEmotion(jason.get('text')) + ':' + jason.get('text'))
        return(True)

    def on_error(self, status):
        print(status)




auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["#Trump"])

