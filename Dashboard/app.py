from flask import Flask, render_template, request, make_response
import tweepy
import pandas as pd
import twitter
from tweepy import Stream
from tweepy import StreamListener
import json
from textblob import TextBlob
import re
import csv
import pickle
from time import time
import random
from datetime import datetime



CONSUMER_KEY = 'x0g63NaebTlGAtpZ2I0Znp6U8'
CONSUMER_SECRET = 'RKTGvBZu7NOu3efWZcnG8zijxNtJoEWzlqS6xLrWyLq0Kv62D2'
OAUTH_TOKEN = '865991910-pqqZNmQINLl5Cju0r3MtFsVhjfJAicz6wQKDuTzg'
OAUTH_TOKEN_SECRET = 'iaqecW3bcPi7BAGVZlTTYABIyqQRt64Fec4sOGv0Oa736'


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

api = tweepy.API(auth)

auth1 = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth1)

# Getting Trends

WORLD_WOE_ID = 1
US_WOE_ID = 23424977
INDIA_WOE_ID = 23424848
trends = []


text_model = pickle.load(open('text.pkl','rb'))

app = Flask(__name__)


hashtagin = ""


ind=0

jnd=0

    
@app.route("/",methods=["GET", "POST"])
def home():
    global ind,jnd
    ind = 0
    jnd = 0
    senti = pd.read_csv('D:/6th Semester/Capstone Project/Dashboard/sentiment.csv')
    header = senti.columns
    q = header[0] 

    count = 100

    # Import unquote to prevent url encoding errors in next_results
    from urllib.parse import unquote

    search_results = twitter_api.search.tweets(q=q, count=count)

    statuses = search_results['statuses']


    # Iterate through 5 more batches of results by following the cursor
    for _ in range(5):
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError as e: # No more results when next_results doesn't exist
            break
        
        # Create a dictionary from next_results, which has the following form:
        # ?max_id=847960489447628799&q=%23RIPSelena&count=100&include_entities=1
        kwargs = dict([ kv.split('=') for kv in unquote(next_results[1:]).split("&") ])
    
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']
    
    
    india_trends = twitter_api.trends.place(_id=INDIA_WOE_ID)
    count = 0
    for trend in india_trends[0]['trends']:
        trends.append(trend['name'])
        count+=1
        if count >20:
            break
        
        
    status_texts = [ status['text'] 
                 for status in statuses ]
    tweetlist = []
    for i in range(len(status_texts)):
        tweet = str(status_texts[i])
        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        tweet = ' '.join(re.sub('RT',' ', tweet).split())
        tweetlist.append(tweet)
    tweet_list = []
    num = 0
    for i in tweetlist:
        tweet_list.append(i)
        num+=1
        if num >20:
            break
  
    
    screen_names = [ user_mention['screen_name'] 
                 for status in statuses
                     for user_mention in status['entities']['user_mentions'] ]
    
    mentions = str(screen_names)
    mention = (mentions[:len(mentions)//10])
    
    hashtags = [ hashtag['text'] 
             for status in statuses
                 for hashtag in status['entities']['hashtags'] ]
    
    hashtags = str(hashtags)
    hashtag1 = (hashtags[:len(hashtags)//10])
        
    return render_template('index.html', list=trends, text=tweet_list, mention=mention, hashtag1=hashtag1)



@app.route('/freq1', methods=["GET", "POST"])
def freq1():
    data1 = [time() * 1000, random.randint(0,20)]
    response1 = make_response(json.dumps(data1))
    response1.content_type = 'application/json'
    return response1


@app.route('/senti2', methods=["GET", "POST"])
def senti2():
    data2 = [time() * 1000, random.uniform(-1,1)]
    response2 = make_response(json.dumps(data2))
    response2.content_type = 'application/json'
    return response2



hashtag_senti = 0
hashtag_freq = 0


@app.route('/hashtag', methods=['POST'])
def twitter():
    global hashtagin
    hashtagin = request.form['a']

    hashtag = hashtagin
    

    header_name = [hashtag]
    #headr_name = [hashtag, 'Time']
    
    with open('D:/6th Semester/Capstone Project/Dashboard/sentiment.csv','w') as file:
        writer = csv.DictWriter(file, fieldnames = header_name)
        writer.writeheader()
    
    with open('D:/6th Semester/Capstone Project/Dashboard/frequency.csv','w') as file:
        writer = csv.DictWriter(file, fieldnames = header_name)
        writer.writeheader()

    class Listener(StreamListener):
    
        def on_data(self, data):
            raw_tweets = json.loads(data)
            tweets = raw_tweets['text']
        
            tweets = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweets).split())
            tweets = ' '.join(re.sub('RT',' ', tweets).split())
        
            blob = TextBlob(tweets.strip())
        
            global hashtag_senti
            global hashtag_freq
                 
            hashtag_sentiment = 0
            hashtag_frequency = 0
            count = 0
            for sent in blob.sentences:
                if hashtag in sent:
                    hashtag_sentiment += sent.sentiment.polarity
                    hashtag_frequency +=  1
                    count += 1
        
            hashtag_senti = hashtag_sentiment/count
            hashtag_freq = hashtag_frequency
        
            with open('D:/6th Semester/Capstone Project/Dashboard/sentiment.csv','a') as file:
                writer = csv.DictWriter(file, fieldnames=header_name)
                #now = datetime.now()
                info = {
                        #'Time': now,
                        hashtag : hashtag_senti
                        }
                writer.writerow(info)
            
            with open('D:/6th Semester/Capstone Project/Dashboard/frequency.csv','a') as file:
                writer = csv.DictWriter(file, fieldnames=header_name)
                #now = datetime.now()
                info = {
                        #'Time': now,
                        hashtag : hashtag_freq
                        }
                writer.writerow(info)
    
        def on_error(self, status):
            print(status)
            
    twitter_stream = Stream(auth, Listener())
    twitter_stream.filter(track = [hashtag], is_async=True)
    
           
    return render_template('live.html')




@app.route('/sentiment', methods=["GET", "POST"])
def sentiment():
    global ind
    sentim = pd.read_csv('D:/6th Semester/Capstone Project/Dashboard/sentiment.csv')
    headr = sentim.columns
    y = sentim[headr[0]].values.tolist()
    data = [time() * 1000, random.uniform(-1,1)]
    ind+=1
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@app.route('/frequency', methods=["GET", "POST"])
def frequency():
    global jnd
    freq = pd.read_csv('D:/6th Semester/Capstone Project/Dashboard/frequency.csv')
    head = freq.columns
    fx = freq[head[0]].values.tolist()
    data = [time() * 1000, random.randint(0,10)]
    jnd+=1
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/text_prediction",methods=["GET", "POST"])
def text_prediction():
    a = request.form['a']
    a = str(a)
    x_test = [a]
    model = pickle.load(open('model.pkl','rb'))
    
    val = model.predict(x_test)
    val = int(val)
    
    return render_template('text.html',data=val, text=a)
    
@app.route("/audio")
def audio():
    return render_template('audio.html')

@app.route("/login")
def login():
    return render_template('login.html')



import os
from werkzeug.utils import secure_filename
app.config['UPLOAD_FOLDER'] = 'D:/6th Semester/Capstone Project/Audio Data/voice commands/'
import speech_recognition as sr

@app.route("/uploader" , methods=['GET', 'POST'])
def uploader():
    if request.method=='POST':
        f = request.files['file1']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    
    r = sr.Recognizer() 
    filepath='D:/6th Semester/Capstone Project/Audio Data/voice commands'
    with sr.AudioFile(filepath + '/' + f.filename) as source:
        audio  = r.listen(source)
        text = r.recognize_google(audio)
    
    blo = TextBlob(text.strip())
    pred = []
    for txt in blo.sentences:
        pred.append(txt.sentiment.polarity)
    
    val = min(pred)
    if val < 0:
        ans = 0

    if val > 0:
        ans = 2 

    return render_template('text.html',data=ans,text=text)

import easyocr
import torch
# Model Saved
MODEL_PATH = './DLmodel.pth'

# Load your trained model
model = torch.load(MODEL_PATH)

def model_predict(img_path, model):
    
    reader = easyocr.Reader(['en'], gpu = False)
    result = reader.readtext(img_path,paragraph="False")

    text = ""
    for detection in result: 
        text = text + " " + detection[1]

    output = model.classify(img_path,text)
    hateful = "Yes" if output["label"] == 1 else "No"

    return hateful


@app.route('/img_predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

        return render_template('img.html',data=preds)
    return None
    

app.run(host= '127.0.0.1', port = 5000, debug=True)
