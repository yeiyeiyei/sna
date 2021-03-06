#!/usr/bin/env python3

# Ideas:
# https://towardsdatascience.com/python-identifying-twitter-influencers-through-network-analysis-964c9b293e03

#
# Imports
#

#
# Start Spark
#
#spark = SparkSession\
#  .builder \
#  .appName("InfluencerGraph") \
#  .getOrCreate()

#
# Tweepy: TweetGrabber
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
        API_results = self.api.search(q=keyword,rpp=100,show_user=True,tweet_mode='extended')

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

#
# Tweepy: Instantiate Classes & Method
#
t = TweetGrabber(
    myApi = 'feboPC8kaZZZwklorde9wLc86',
    sApi = 'iuCs9eIjQnFZXMl7kXUAJUMIilTVmgeHXp5S36cGdfJD5EWz09',
    at = '14910859-fuoIx35dmEm0ZnivKZOajAbS7ngTiQmbEumzqQ2so',
    sAt = 'Gzhz3ugN6DymzrdqmAWWOpWguPWowrmDCo1VlfPA32y9E'
    )
#t.user_search(user='Tesla',csv_prefix='tesla_tweets')
#t.user_search(user='elonmusk',csv_prefix='elonmusk_tweets')
#t.keyword_search(keyword='Tesla',csv_prefix='key_tesla_tweets')


#
# Cleaning & Edges
#
#Variable to hold whatever Twitter user is being classified
#screen_name = "screen_name"

class RetweetParser():

    def __init__(self,data,user):
        import ast
        self.user = user

        edge_list = []

        for idx,row in data.iterrows():
            if len(row[4]) > 5:
                user_account = user
                weight = np.log(row[5] + 1)
                for idx_1, item in enumerate(ast.literal_eval(row[4])):
                    edge_list.append((user_account,item['screen_name'],weight))

                    for idx_2 in range(idx_1+1,len(ast.literal_eval(row[4]))):
                        name_a = ast.literal_eval(row[4])[idx_1]['screen_name']
                        name_b = ast.literal_eval(row[4])[idx_2]['screen_name']

                        edge_list.append((name_a,name_b,weight))

        import csv
        with open(f'{self.user}.csv', 'w', newline='') as csvfile:
            fieldnames = ['user_a', 'user_b', 'log_retweet']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in edge_list:
                writer.writerow({
                                'user_a': row[0],
                                'user_b': row[1],
                                'log_retweet': row[2]
                                })

#r = RetweetParser(,'user_b')
#r = RetweetParser(data,'elonmusk_tweets')
r = RetweetParser('elonmusk_tweets.csv','elon_tweets.csv')


#
# Class
#
class TweetGraph():

    def __init__(self,edge_list):
        import igraph
        import pandas as pd
        data = pd.read_csv(edge_list).to_records(index=False)
        self.graph = igraph.Graph.TupleList(data, weights=True, directed=False)

    def e_centrality(self):
        import operator
        vectors = self.graph.eigenvector_centrality()
        e = {name:cen for cen, name in  zip([v for v in vectors],self.graph.vs['name'])}
        return sorted(e.items(), key=operator.itemgetter(1),reverse=True)


m_graph = MyGraph(edge_list='elon_tweets.csv')
m_graph.e_centrality()


#
# Stop Spark
#
#spark.stop()
