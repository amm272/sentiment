# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 08:31:54 2020

@author: User

References: https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/

"""
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob  
import pandas as pd
import sklearn as skl
from sklearn.naive_bayes import MultinomialNB
from nltk.tokenize import word_tokenize
from string import punctuation
import nltk 
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import RegexpTokenizer

#dataset = pd.read_excel(r'C:\Users\User\Desktop\Ana-Maria\University\Machine Learning\Sentiment Analysis\2477_4140_bundle_archive\training.1600000.processed.xlsx', usecols = 'A,F', nrows = 100);

X = pd.DataFrame(dataset.loc[:,'text'])
y = pd.DataFrame(dataset.loc[:,'label'])

features = X.values
labels = y.values

api = TwitterClient()

processed_features = []
for sentence in range(0, len(features)):
    processed_feature = api.clean_tweet(str(features[sentence]))  
    processed_feature = word_tokenize(processed_feature)     
    processed_features.append(processed_feature)

print(processed_features)

#X = pd.DataFrame(['happy hour', 'why are you sad', 'blob is good $#@', 'no', 'yes', 'hakuna matata', 'nestle', 'tree', 'boob', 'tomorrow', 'car manufacturer','flower is beauty','@georgia baby boomers','turm of sheeps!','camera man'])
#y = pd.DataFrame([1,0,1,0,1,1,0,1,1,1,0,1,1,1,0])

X_train, X_test, y_train, y_test = skl.model_selection.train_test_split(X, y, test_size=0.2, random_state=1);
X_train, X_val, y_train, y_val = skl.model_selection.train_test_split(X_train, y_train, test_size = 0.25, random_state=1)

class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'XXXXXXXXXXXXXXXXXXXX';
        consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXX';
        access_token = 'XXXXXXXXXXXXXXXXXXXX';
        access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXX';
  
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
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet))
        
        # set sentiment
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        elif analysis.sentiment.polarity < 0: 
            return 'negative'
  
    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query + '-filter:retweets', count = count) 
  
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 
  
                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
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
            

def CleanData(data):    
    return data
            
def NaiveBayesTrain(tweet):
    tweet = word_tokenize(tweet); 
    return tweet

def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient()
    # calling function to get tweets 
    tweets = api.get_tweets(query = 'coronavirus', count = 100) 
    
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
    for tweet in ptweets[:10]: 
        print(api.clean_tweet(tweet['text'])) 
  
    # printing first 5 negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:10]: 
        print(api.clean_tweet(tweet['text'])) 
  
#if __name__ == "__main__": 
#    # calling main function 
#    main()
  
