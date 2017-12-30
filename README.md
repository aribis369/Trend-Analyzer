# Trend-Analyzer
Analyses trends in upcoming movie's anticipation.

This project analyzes trends in movie anticipation by scraping data from IMDb and twitter and then performing sentiment analysis
on tweets to identify positive tweets. Finally plotting this time series data to identify patterns in movie anticipation.

The workflow takes place in three steps:-
1. Scraping of data<br/>
	In the scraper folder of the repo there are two scripts for scraping:<br/>
	a) <b>movies.py</b> - to scrape the popularity of movies from IMDb and store it in mongodb.<br/>
		       (This is code is run from crontab every 10 minutes)<br/>
	b) <b>tweets.py</b> - to scrape tweets from twitter and string it in a text file.

2. Modeling<br/>
	In the models folder of the repo we have three scripts for modeling:<br/>
	a) <b>sentiment_analysis.py</b> - to perform sentiment analysis of extracted tweets and find out the percentage of positive tweets pertaining to a movie.<br/>
	b) <b>sent_pre_trained_naive_Bayes.py</b> - to train a Naive Bayes model on the training data and store the model as an object so that we don't have to train the model everytime we perform sentiment analysis.<br/>
	c) <b>sent_predict.py</b> - to predict the sentiment of the extracted tweets using the pretrained model and store the percentage of positive tweets for movies in mongodb.<br/>
			     (This is code is run from crontab every 10 minutes)

3. Visualization<br/>
	In the visualization folder of the repo we have two scripts to perform visualization of time series data:<br/>
	a) <b>visualization.py</b> - to visualize the popularity of movies on the basis of data extracted from IMDb using the script movies.py by plotting it against time.<br/>
  <img src='https://github.com/aribis369/Trend-Analyzer/blob/master/figures/IMDb_vis_Tiger%20Zinda%20Hai.png' />
	b) <b>visuallize_timeseries.py</b> – to visualize the percentage of positive tweets for different movies stored in mongodb by sent_predict.py by plotting it against time.<br/>
  <img src='https://github.com/aribis369/Trend-Analyzer/blob/master/figures/tweets_vis_TigerZindaHai.png

All the visualization figures are stored in the figures folder of the repo.
