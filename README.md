# TweetsGrabber
Creates a csv of all tweets from a given twitter handle, uses Tweepy

## Usage
```
python grab_tweets.py <user_handle>
	-user_handle: the handle of the user we are grabbing tweets from
```

### The application will automatically halt based on the Twitter API's rate-limiting. If the application seems to be halting progress, simply wait and it should continue progress within 15 minutes.

## Note: The text of Retweeted tweets will be truncated, due to a limit in the twitter api.

#### This application also requires a configuration file named 'tweepy_config' with four lines of text representing the consumer_key, consumer_secret, access_token, and access_token_secret, respectively. For details, consult [the tweepy documentation.](https://tweepy.readthedocs.io/en/latest/auth_tutorial.html)
