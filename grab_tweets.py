import tweepy
import sys
import traceback
import os
import csv
import pandas as pd

def show_usage():
    print("python grab_tweets.py <user_handle>")
    print("\tuser_handle: the handle of the user we are grabbing tweets from")
    print()
    print("This application also requires a configuration file named 'tweepy_config' with four lines of text representing the consumer_key, consumer_secret, access_token, and access_token_secret, respectively. For details, consult the tweepy documentation.")
    print()

def get_profile(api, this_handle):
    profile = api.get_user(screen_name=this_handle)
    if profile is None:
        print("The given profile (" + this_handle + ") does not exist.")
        raise Exception
    return profile

def get_tweets(api, profile):
    data = []

    #below section adopted from yanofsky
    #https://gist.github.com/yanofsky/5436496
    #This script extends on the logic of yanofsky by creating a pandas dataframe for easier analysis
    all_tweets = []  
    new_tweets = api.user_timeline(screen_name=profile.screen_name, include_rts=False, count=200, tweet_mode='extended')
    all_tweets.extend(new_tweets)
    oldest = all_tweets[-1].id - 1
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name=profile.screen_name, count=200, max_id=oldest, include_rts=False, tweet_mode='extended')
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1
    #end section adopted from yanofsky

    for tweet in all_tweets:
        data.append([tweet.full_text, tweet.favorite_count, tweet.retweet_count, tweet.created_at])

    tweets = pd.DataFrame(data, columns = ['text', 'favorite_count', 'retweet_count', 'created_at'])
    tweets = tweets.set_index('created_at')

    print("==============================")
    print(tweets)
    print("==============================")

    return tweets

try:
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''

    with open('tweepy_config') as config_file:
        consumer_key = config_file.readline().strip()
        consumer_secret = config_file.readline().strip()
        access_token = config_file.readline().strip()
        access_token_secret = config_file.readline().strip()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    profile = get_profile(api, sys.argv[1])

    tweets = get_tweets(api, profile)

    tweets.to_csv(profile.screen_name +'_tweets.csv', encoding='utf-8-sig')

    print("Tweets saved to " + profile.screen_name + '_tweets.csv')
    print("==========================")
    print("Completed.")

except:
    traceback.print_exc()
    print("\n==========================================\n")
    show_usage()