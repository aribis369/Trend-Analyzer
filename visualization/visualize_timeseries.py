# This is a code to visualize the data stored in mongodb using pandas and matplotlib
# This visualization code is specific to the movie "Tiger Zinda Hai"
# This code can be used to visualize the percentage of positive tweets for any movie by just changing the values
# First the data stored is retrieved inside a cursor
# Then for every document that is retrieved we specifically extract the percentage tweets of the desired movie
# Then using pandas library we store it in a pandas DataFrame to plot it

from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt


def main():
	perc_list = []					# list that stores the percentage of positive tweets
	time_list = []					# list that stores the time at which data was extracted

	# retrieve the data from mongodb
	col = MongoClient()
	result = col.tweet_sent.twitter_data.find()
	for doc in result:
		for key in doc:
			if key!="_id":
				perc_list.append(doc[key]['perc'])
				time_list.append(doc[key]['time'])

	# storing data in a pandas DataFrame and plotting
	df = pd.DataFrame((perc_list),index=time_list)
	df.plot()
	
	# plotting the data
	plt.title('Plot for Positive Tweets vs Time for movie: Tiger Zinda Hai', fontsize='20', style='oblique')
	plt.xlabel('Time', fontsize='16', color='green')
	plt.ylabel('Percentage positive tweets', fontsize='16', color='green')
	plt.show()

if __name__ == "__main__":
	main()