#!/usr/bin/env python

# This code first extracts top 100 tweets for a movie, then predicts the sentiment for those tweets, calculates the percentage of
# positive tweets and then stores this data alongwith timestamp into mongodb.
# Run this code using crontab for say every 10 mins
# This code uses Naive Bayes Classifier, the model for which was trained in "sent_pre_trained_naive_Bayes.py" script,
# to classify tweets as positive or negative

import json
import pandas as pd
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import classification_report
from sklearn.externals import joblib
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import pymongo
import datetime

#Variables that contains the user credentials to access Twitter API 
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

tweets_data = []

# Preprocess the extracted tweets to be predicted by the model
def preprocess(tweets_data):
    count_vectorizer = joblib.load('../data/vectorizer.pkl')		# when running with crontab use absolute path
    tweets_data = count_vectorizer.transform(tweets_data)
    tfidf_tweet = TfidfTransformer(use_idf=False).transform(tweets_data)		# Tf-idf matrix for tweets
    return tfidf_tweet

# learning the naive bayes classifier to classify the data
def predict_sentiment(tweets_data):
    classifier = joblib.load('../data/Naive_Bayes.pkl')			# when running with crontab use absolute path
    predicted_tweets = classifier.predict(tweets_data)
    return predicted_tweets

# Compute current date and time
def time():
	time_str = str(datetime.datetime.now())
	time_list = time_str.split(" ")
	# The first element of the list stores the date and second element stores time
	return time_str,time_list

def main():
	
	# code for authorization
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = API(auth)
	tweets_list = api.search(q='TigerZindaHai', count=100)				# retrieve top 100 tweets for the movie
	for tweet in tweets_list:
		tweets_data.append(tweet.text)

	# Preprocessing tweets to give as input to the classifier
	tfidf_tweet = preprocess(tweets_data)

	# Predicted output received from the classifier
	predicted_output = predict_sentiment(tfidf_tweet)

	pos_count = 0
	neg_count = 0

	# Checking whether the tweet has a positive or negative sentiment
	for i in range(len(tweets_data)):
		if predicted_output[i]=='1':
			sent="Positive"
			pos_count=pos_count+1
		else:
			sent="Negative"
			neg_count=neg_count+1
		
	# Displaying statistics
	print("Total tweets: %d") %(i+1)
	print("Positive tweets: %d") %(pos_count)
	print("Negative tweets: %d") %(neg_count)
	perc_pos = float(pos_count)/(i+1)*100
	print("Percentage of positive tweets: %f%%") %(perc_pos)

	time_str,time_list = time()
	
	# Creating appropriate data structure to store in mongodb
	dic = {}
	dic["perc"] = perc_pos
	dic["date"] = time_list[0]
	dic["time"] = time_list[1]
	print(dic)
	pos_dict = {}
	pos_dict[time_str] = dic
	print(pos_dict)

	# Storing this information in mongodb for time series visualization
	client = pymongo.MongoClient()
	db = client.tweet_sent
	db.twitter_data.insert(pos_dict,check_keys=False)
	
if __name__ == "__main__":
	main()
