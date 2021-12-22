
#%%
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 08:31:54 2020

@author: Ana-Maria Marcu

References: https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/

"""
import pandas as pd
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob  
from nltk.tokenize import word_tokenize
import os
from dotenv import load_dotenv
from textblob.sentiments import NaiveBayesAnalyzer

class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # load environment variables
        load_dotenv()
        # keys and tokens from the Twitter Dev Console 
        consumer_key = os.getenv('CONSUMER_KEY')
        consumer_secret = os.getenv('CONSUMER_SECRET')
        access_token = os.getenv('ACCESS_TOKEN')
        access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
        bearer_token = os.getenv('BEARER_TOKEN')

        # attempt authentication 
        try: 
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.Client(bearer_token = bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        
        # Remove all usernames
        tweet = re.sub(r'@[^\s]+', ' ', tweet)
        
        # Remove all special characters
        tweet = re.sub(r'\W', ' ', tweet)
        
        # Remove all single characters
        tweet = re.sub(r'\s+[a-zA-Z]\s+', ' ', tweet)

        # Remove single characters from the start
        tweet = re.sub(r'\^[a-zA-Z]\s+', ' ', tweet) 
                
        # Remove all digits
        tweet = re.sub("^\d+\s|\s\d+\s|\s\d+$", ' ', tweet)
        tweet = re.sub("\d+",' ', tweet)

        # Substituting multiple spaces with single space
        tweet = re.sub(r'\s+', ' ', tweet, flags=re.I)

        # Removing prefixed 'b'
        tweet = re.sub(r'^b\s+', '', tweet)
        
        # Converting to lowercase
        tweet = tweet.lower()
        
        return tweet;
 
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using a Naive Bayes classifier trained on a movie corpora method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet), analyzer = NaiveBayesAnalyzer())
        
        # set sentiment
        if analysis.sentiment[1]==0.5: 
            return 'neutral'
        elif analysis.sentiment[0] == 'pos': 
            return 'positive'
        elif analysis.sentiment[0] == 'neg': 
            return 'negative'
  
    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        #try: 
        print('Trying tweets fetching')
            # call twitter api to fetch tweets 
        fetched_tweets = self.api.search_recent_tweets(query=query, max_results=count).data
        # parsing tweets one by one 
        for tweet in fetched_tweets:
            # empty dictionary to store required params of a tweet 
            parsed_tweet = {} 
  
            # saving text of tweet 
            parsed_tweet['text'] = tweet.text 
            # saving sentiment of tweet 
            parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
            # appending parsed tweet to tweets list 
            if parsed_tweet not in tweets: 
                tweets.append(parsed_tweet) 
            else: 
                tweets.append(parsed_tweet) 
  
            # return parsed tweets 
        return tweets 
  
        #except: 
            # print error (if any) 
        #    print("Error: tweet fetching failed.")
        #    print("Note: to run this code from GitHub you will need your valid API credentails.")            

def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient()

    # calling function to get tweets 
    tweets = api.get_tweets(query = 'coronavirus', count = 10) 

    try:
    # picking positive tweets from tweets 
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
        # percentage of positive tweets 
        print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
        # picking negative tweets from tweets 
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
        # percentage of negative tweets 
        print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
        # percentage of neutral tweets 
        print("Neutral tweets percentage: {} %".format(100*(len(tweets)-(len( ntweets )+len( ptweets)))/len(tweets))) 
  
        # printing first 5 positive tweets 
        print("\n\nPositive tweets:") 
        for tweet in ptweets[:5]: 
            print(api.clean_tweet(tweet['text'])) 
  
        # printing first 5 negative tweets 
        print("\n\nNegative tweets:") 
        for tweet in ntweets[:5]: 
            print(api.clean_tweet(tweet['text']))
    except:
        if(tweets==None):
            print('No tweets fetched.')
        else:
            print('Error: sentiment calculation unsuccessful.') 
  
if __name__ == "__main__": 
    # calling main function 
    main()
# %%
