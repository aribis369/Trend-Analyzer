# This is a code to visualize the data stored in mongodb using pandas and matplotlib
# This visualization code is specific to the movie "Tiger Zinda Hai"
# We visualize the rating of the movie as shown on IMDB over the period of time and plot it on a graph
# First the data stored is retrieved inside a cursor
# Then for every document that is retrieved we specifically extract the rating of the desired movie
# Then using pandas library we store it in a pandas DataFrame to plot it

from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt


def main():
	rating_list = []				# list that stores the rating of the desired movie
	time_list = []					# list that stores the time at which data was extracted

	# retrieve the data from mongodb
	col = MongoClient()["movierating"]["movieratings"]
	result = col.find()

	# for each document extract the rating and of desired movie
	for doc in result:
		if doc['Tiger Zinda Hai']['time']!='':
			rating_list.append(float(doc['Tiger Zinda Hai']['share'][:-1]))
			time_list.append((doc['Tiger Zinda Hai']['time']))

	# storing data in a pandas DataFrame and plotting
	df = pd.DataFrame((rating_list),index=time_list)
	df.plot()
	plt.show()

if __name__ == "__main__":
	main()