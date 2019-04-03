#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import csv #Import csv
#Variables that contains the user credentials to access Twitter API 
access_token = "1099383062482350080-FHN9RBJBMtpxOOn9f927Sx7KNqbwYB"
access_token_secret = "air4z8lDDxs2O2Ta41VHqPi9tzFhthhjKeZUoUcDH7nCO"
consumer_key = "eLIVR0fk7DHynUmAZjpcgwjHT"
consumer_secret = "zRBvz1W33BkH8Lf1JwURwEcMoTia5zSMNrtSr3yxa1uaZfenVs"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    csvFile = open('result.csv', 'a')

#Use csv writer
    csvWriter = csv.writer(csvFile, dialect='excel')
    def on_data(self, data):
        print(data)
        #csvWriter.writerow(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)


    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['indiannews','indianelectionnews','indianprotests','protestsin india','riots in india','indian political news','indian law enforcement','indian activists','indian NGOs','indian Farmers','RSS india'])