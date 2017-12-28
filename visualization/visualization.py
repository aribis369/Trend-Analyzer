# This is a code to visualize the data stored in mongodb using pandas and matplotlib
# This visualization code plots the popularity of 8 movies
# We visualize the rating of the movie as shown on IMDB over the period of time and plot it on a graph
# First the data stored is retrieved inside a cursor
# Then for every document that is retrieved we specifically extract the rating of the desired movie
# Then using pandas library we store it in a pandas DataFrame to plot it
# A function is used to convert the date to a suitable format

from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

month_dict = {
	'01':'Jan',
	'02':'Feb',
	'03':'Mar',
	'04':'Apr',
	'05':'May',
	'06':'Jun',
	'07':'Jul',
	'08':'Aug',
	'09':'Sep',
	'10':'Oct',
	'11':'Nov',
	'12':'Dec'
}

movie_list = ['Tiger Zinda Hai','Sonu Ke Titu Ki Sweety','Padman','1921','Thaanaa Serndha Koottam','Fukrey Returns','Mukkabaaz','Monsoon Shootout']

# A typical time_str would look like "2017-12-03 13:36:35+00:00"
# The code converts this string into a more user-friendly and convenient format
# The format after conversion looks like "03 Dec 13:36"
def timestamp(time_str):
	t_list = time_str.split()
	t1_list = t_list[0].split("-")
	t2_list = t_list[1].split(":")
	t = t1_list[2]+" "+month_dict[t1_list[1]]+" "+t2_list[0]+":"+t2_list[1]
	return t

def main():
	for item in movie_list:
		rating_list = list()				# list that stores the rating of the desired movie
		time_list = list()					# list that stores the time at which data was extracted

		# retrieve the data from mongodb
		col = MongoClient()["movierating"]["movieratings"]
		result = col.find()

		# for each document extract the rating and of desired movie
		for doc in result:
			if item in doc:
				if doc[item]['time']!='':
					rating_list.append(float(doc[item]['share'][:-1]))
					time_list.append(timestamp(str(doc['_id'].generation_time)))

		# storing data in a pandas DataFrame and plotting
		df = pd.DataFrame((rating_list),index=time_list)
		df.plot()
		
		# plotting the data
		plt.title('Plot for Popularity vs Time for movie: '+item, fontsize='20', style='oblique')
		plt.xlabel('Time', fontsize='16', color='green')
		plt.ylabel('Percentage popularity', fontsize='16', color='green')
		plt.savefig('../figures/IMDb_vis_'+item+'.png')
		plt.show()

if __name__ == "__main__":
	main()