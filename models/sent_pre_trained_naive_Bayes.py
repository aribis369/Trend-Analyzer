# This python script trains a Naive Bayes Classifier on labelled dataset and stores the relevant model as file

# Download the training data from here thinknook.com/wp-content/uploads/2012/09/Sentiment-Analysis-Dataset.zip and store it in data folder

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

def preprocess(data):
    # data,target = load_from_csv()
    count_vectorizer = CountVectorizer(binary='true')
    data = count_vectorizer.fit_transform(data)
    tfidf_train = TfidfTransformer(use_idf=False).fit_transform(data)			# Tf-idf matrix for training data

    # Storing the vectorizer as well because the training data has many features as compared to test data, so when we take a new 
    # vectorizer in prediction code, during classification it will produce error as insufficient features.
    # Hence we need to use the same vectorizer as we used during training
    joblib.dump(count_vectorizer,'../data/vectorizer.pkl')								
    return tfidf_train

# learning the naive bayes classifier to classify the data
def learn_model(data,target):
    classifier = BernoulliNB().fit(data,target)
    joblib.dump(classifier, '../data/Naive_Bayes.pkl')								# Store the learned model as a file for using later
    
# main function
def main():
	
	data,target = load_from_csv()
	
	# Preprocessing both labelled and unlabelled tweets to give as input to the classifier
	tfidf_train = preprocess(data)

	# Learning the training model
	learn_model(tfidf_train,target)
	
	print "Model learned successfully"

if __name__ == "__main__":
	main()