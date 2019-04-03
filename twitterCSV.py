#!/usr/bin/python
import tweepy
import csv #Import csv
auth = tweepy.auth.OAuthHandler('eLIVR0fk7DHynUmAZjpcgwjHT', 'zRBvz1W33BkH8Lf1JwURwEcMoTia5zSMNrtSr3yxa1uaZfenVs')
auth.set_access_token('1099383062482350080-FHN9RBJBMtpxOOn9f927Sx7KNqbwYB', 'air4z8lDDxs2O2Ta41VHqPi9tzFhthhjKeZUoUcDH7nCO')

api = tweepy.API(auth)

# Open/create a file to append data to
csvFile = open('result.csv', 'a')

#Use csv writer
csvWriter = csv.writer(csvFile)

for tweet in tweepy.Cursor(api.search,
                           q = ["IndianPolitics","riots","protests","rallies","elections"],
                           since = "2014-02-14",
                           until = "2014-02-15",
                           lang = "en").items():

    # Write a row to the CSV file. I use encode UTF-8
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
    print(tweet.created_at, tweet.text)
csvFile.close()