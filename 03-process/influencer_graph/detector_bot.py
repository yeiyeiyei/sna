#!/usr/bin/env python3

# Ideas:
# https://towardsdatascience.com/python-detecting-twitter-bots-with-graphs-and-machine-learning-41269205ab07

#
# Imports
#

#
# Classes: TweetGrabber
#
#
class TweetGrabber():

    def __init__(self,myApi,sApi,at,sAt):
        import tweepy
        self.tweepy = tweepy
        auth = tweepy.OAuthHandler(myApi, sApi)
        auth.set_access_token(at, sAt)
        self.api = tweepy.API(auth)


    def strip_non_ascii(self,string):
        ''' Returns the string without non ASCII characters'''
        stripped = (c for c in string if 0 < ord(c) < 127)
        return ''.join(stripped)

    def keyword_search(self,keyword,csv_prefix):
        import csv
        API_results = self.api.search(q=keyword,rpp=1000,show_user=True,tweet_mode='extended')

        with open(f'{csv_prefix}.csv', 'w', newline='') as csvfile:
            fieldnames = ['tweet_id', 'tweet_text', 'date', 'user_id', 'follower_count',
                          'retweet_count','user_mentions']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for tweet in API_results:
                text = self.strip_non_ascii(tweet.full_text)
                date = tweet.created_at.strftime('%m/%d/%Y')
                writer.writerow({
                                'tweet_id': tweet.id_str,
                                'tweet_text': text,
                                'date': date,
                                'user_id': tweet.user.id_str,
                                'follower_count': tweet.user.followers_count,
                                'retweet_count': tweet.retweet_count,
                                'user_mentions':tweet.entities['user_mentions']
                                })

    def user_search(self,user,csv_prefix):
        import csv
        API_results = self.tweepy.Cursor(self.api.user_timeline,id=user,tweet_mode='extended').items()

        with open(f'{csv_prefix}.csv', 'w', newline='') as csvfile:
            fieldnames = ['tweet_id', 'tweet_text', 'date', 'user_id', 'user_mentions', 'retweet_count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for tweet in API_results:
                text = self.strip_non_ascii(tweet.full_text)
                date = tweet.created_at.strftime('%m/%d/%Y')
                writer.writerow({
                                'tweet_id': tweet.id_str,
                                'tweet_text': text,
                                'date': date,
                                'user_id': tweet.user.id_str,
                                'user_mentions':tweet.entities['user_mentions'],
                                'retweet_count': tweet.retweet_count
                                })

# Twitter API Credentials
access_token = "14910859-fuoIx35dmEm0ZnivKZOajAbS7ngTiQmbEumzqQ2so"
access_token_secret = "Gzhz3ugN6DymzrdqmAWWOpWguPWowrmDCo1VlfPA32y9E"
consumer_key = "feboPC8kaZZZwklorde9wLc86"
consumer_secret = "iuCs9eIjQnFZXMl7kXUAJUMIilTVmgeHXp5S36cGdfJD5EWz09"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
