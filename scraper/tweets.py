# This code extracts tweets from twitter API regarding the movie Tiger Zinda Hai
# To run this code first install twitter API and get token and key to enter below
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""


#This is a basic listener that just prints received tweets to output file.
class StdOutListener(StreamListener):

    def on_data(self, data):
        file = open("../data/extracted_tweets.txt","a")
        file.write(data)
        file.close()
        # print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keyword: TigerZindaHai
    stream.filter(track=['TigerZindaHai'])