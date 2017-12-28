# This is a code to visualize the data stored in mongodb using pandas and matplotlib
# This visualization code plots the percentage of positive tweets for 8 movies
# First the data stored is retrieved inside a cursor
# Then for every document that is retrieved we specifically extract the percentage of positive tweets of the desired movie
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

movie_list = ['TigerZindaHai','SonuKeTituKiSweety','Padman','1921','ThaanaaSerndhaKoottam','FukreyReturns','Mukkabaaz','MonsoonShootout']

# A typical time_str would look like "15:42:00.946931" and time_str like "2017-12-16"
# The code converts this string into a more user-friendly and convenient format
# The format after conversion looks like "03 Dec 13:36"
def timestamp(time_str,date_str):
	t1_list = date_str.split("-")
	t2_list = time_str.split(":")
	t = t1_list[2]+" "+month_dict[t1_list[1]]+" "+t2_list[0]+":"+t2_list[1]
	return t

def main():
	for item in movie_list:
		perc_list = list()					# list that stores the percentage of positive tweets
		time_list = list()					# list that stores the time at which data was extracted

		# retrieve the data from mongodb
		col = MongoClient()
		result = col.tweet_sent.twitter_data.find()
		for doc in result:
			# print doc
			# break
			for key in doc:
				if key!="_id" and 'name' in doc[key]:
					if doc[key]['name']==item:
						perc_list.append(doc[key]['perc'])
						time_list.append(timestamp(doc[key]['time'],doc[key]['date']))
				elif key!="_id" and 'name' not in doc[key] and item=='TigerZindaHai':
					perc_list.append(doc[key]['perc'])
					time_list.append(timestamp(doc[key]['time'],doc[key]['date']))

		# storing data in a pandas DataFrame and plotting
		df = pd.DataFrame((perc_list),index=time_list)
		df.plot()
		
		# plotting the data
		plt.title('Plot for Positive Tweets vs Time for movie: '+item, fontsize='20', style='oblique')
		plt.xlabel('Time', fontsize='16', color='green')
		plt.ylabel('Percentage positive tweets', fontsize='16', color='green')
		plt.savefig('../figures/tweets_vis_'+item+'.png')
		plt.show()

if __name__ == "__main__":
	main()