import sys
sys.path.insert(0, 'GetOldTweets-python')
if sys.version_info[0] < 3:
	import got
else:
	import got3 as got


class TwitterContextSearch(object): 
	def __init__(self): 
		consumer_key = 'eLIVR0fk7DHynUmAZjpcgwjHT'
		consumer_secret = 'zRBvz1W33BkH8Lf1JwURwEcMoTia5zSMNrtSr3yxa1uaZfenVs'
		access_token = '1099383062482350080-FHN9RBJBMtpxOOn9f927Sx7KNqbwYB'
		access_token_secret = 'air4z8IDDxs2O2Ta41VHqPi9tzFhthhjKeZUoUcDH7nCO'

	def printTweet(self, descr, t):
		print(descr)
		print("Username: %s" % t.username)
		print("Retweets: %d" % t.retweets)
		print("Text: %s" % t.text)
		print("Mentions: %s" % t.mentions)
		print("Hashtags: %s\n" % t.hashtags)

	def getTweetsByUserName(self, username, limit):
		tweetCriteria = got.manager.TweetCriteria().setUsername(username).setMaxTweets(limit)
		return got.manager.TweetManager.getTweets(tweetCriteria)

	def searchTweets(self, query, since, until, limit):
		tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setSince(since).setUntil(until).setMaxTweets(limit)
		return got.manager.TweetManager.getTweets(tweetCriteria)

	def getUserTweetsWithDates(self, username, since, until, limit):
		tweetCriteria = got.manager.TweetCriteria().setUsername(query).setSince(since).setUntil(until).setMaxTweets(limit)
		return got.manager.TweetManager.getTweets(tweetCriteria)


# if __name__ == '__main__':
# 	main()