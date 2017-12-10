# This code performs sentiment analysis on the extracted tweets
# Run this code once you have peformed extraction of tweets and stored them in a text file "data/extracted_tweets.txt"
# This code uses Naive Bayes Classifier to classift tweets as positive or negative
# Download the training data from here thinknook.com/wp-content/uploads/2012/09/Sentiment-Analysis-Dataset.zip and store it in data folder

import json
import pandas as pd
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import BernoulliNB
from sklearn import cross_validation
from sklearn.metrics import classification_report
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn import svm

tweets_file = open("../data/extracted_tweets.txt")


# To load data from labelled csv file into lists to preprocess
def load_from_csv():
	training_file = open("../data/Sentiment-Analysis-Dataset.csv")
	data = []
	target = []
	for line in training_file:
		tweet = line.split(",")
		data.append(tweet[3])
		target.append(tweet[1])
	return data,target

# To preprocess data for training classifier
def preprocess(data,tweets_data):
    # data,target = load_from_csv()
    count_vectorizer = CountVectorizer(binary='true')
    data = count_vectorizer.fit_transform(data)
    tfidf_train = TfidfTransformer(use_idf=False).fit_transform(data)			# Tf-idf matrix for training data
    tweets_data = count_vectorizer.transform(tweets_data)
    tfidf_tweet = TfidfTransformer(use_idf=False).transform(tweets_data)		# Tf-idf matrix for tweets
    return tfidf_train,tfidf_tweet

# learning the naive bayes classifier to classify the data
def learn_model(data,target,tweets_data):
    classifier = BernoulliNB().fit(data,target)
    predicted_tweets = classifier.predict(tweets_data)
    return predicted_tweets


def main():
	tweets_data = []

	# Extracting tweets from csv file created using twitter scraper
	for line in tweets_file:
	    try:
	        tweet = json.loads(line)
	        tweets_data.append(tweet['text'])
	    except:
	        continue

	# Getting labelled data from csv file
	data,target = load_from_csv()
	
	# Preprocessing both labelled and unlabelled tweets to give as input to the classifier
	tfidf_train,tfidf_tweet = preprocess(data,tweets_data)

	# Predicted output received from the classifier
	predicted_output = learn_model(tfidf_train,target,tfidf_tweet)

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
		print("Tweet: %s\tSentiment: %s") %(tweets_data[i],sent)

	# Displaying statistics
	print("Total tweets: %d") %(i+1)
	print("Positive tweets: %d") %(pos_count)
	print("Negative tweets: %d") %(neg_count)
	print("Percentage of positive tweets: %f%%") %(float(pos_count)/(i+1)*100)
if __name__ == "__main__":
	main()