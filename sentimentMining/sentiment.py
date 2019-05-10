import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
import csv

class TwitterClient(object): 
	''' 
	Generic Twitter Class for sentiment analysis. 
	'''
	def __init__(self): 
		''' 
		Class constructor or initialization method. 
		'''
		# keys and tokens from the Twitter Dev Console 
		consumer_key = 'eLIVR0fk7DHynUmAZjpcgwjHT'
		consumer_secret = 'zRBvz1W33BkH8Lf1JwURwEcMoTia5zSMNrtSr3yxa1uaZfenVs'
		access_token = '1099383062482350080-FHN9RBJBMtpxOOn9f927Sx7KNqbwYB'
		access_token_secret = 'air4z8IDDxs2O2Ta41VHqPi9tzFhthhjKeZUoUcDH7nCO'

		# attempt authentication 
		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		''' 
		Utility function to clean tweet text by removing links, special characters 
		using simple regex statements. 
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", tweet).split()) 

	def get_tweet_sentiment(self, tweet): 
		''' 
		Utility function to classify sentiment of passed tweet 
		using textblob's sentiment method 
		'''
		# create TextBlob object of passed tweet text 
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def read_tweets(self):
		tweets = []
		with open('output_got.csv', 'r', newline='') as csvfile:
			reader = csv.DictReader(csvfile, delimiter=';')
			for tweet in reader:
				tweets.append(tweet)
		return tweets

	def feature_extract(self, tweets_read): 
		''' 
		Main function to fetch tweets and parse them. 
		'''
		# empty list to store parsed tweets 
		tweets = [] 

		try: 
			fetched_tweets = tweets_read
			# parsing tweets one by one 
			for tweet in fetched_tweets: 
				# empty dictionary to store required params of a tweet 
				parsed_tweet = {} 

				# saving text of tweet 
				parsed_tweet['text'] = tweet.text 
				# saving sentiment of tweet 
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

				# appending parsed tweet to tweets list 
				if int(tweet.retweets) > 0: 
					# if tweet has retweets, ensure that it is appended only once 
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 

			# return parsed tweets 
			return tweets 

		except tweepy.TweepError as e: 
			# print error (if any) 
			print("Error : " + str(e)) 

def getSentimentFeature(tweets): 
	# creating object of TwitterClient Class 
	api = TwitterClient() 
	# calling function to get tweets 
	tweets = api.feature_extract(tweets)
	# picking positive tweets from tweets 
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
	# picking negative tweets from tweets 
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

	#return positive, negative and neutral percentages
	return (100*len(ptweets)/len(tweets),100*len(ntweets)/len(tweets),100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))
# if __name__ == "__main__": 
# 	# calling main function 
# 	main() 
