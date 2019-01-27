import tweepy
import json
from textblob import TextBlob
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
consumer_key= 'mupucnuirYgcDUcdoWnbKI5Sj'
consumer_secret= 'bOkWp3ysvnlr3Zw9bzFNPTVK0TijLSbFaU9MKrWUZSRJ9wIxLN'
access_token='812697466990641152-qO3nshDugAhzCu2e8wihgUYnc5ricqC'
access_token_secret='edXnxrMcjJOJgS8biXrAprAxUCNM5nhiUJUT7C3dsac2U'


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        for url in tweet["entities"]["urls"]:
            print (" - found URL: %s" % url["expanded_url"])
        return True

    def on_error(self, status):
        print (status)


# Given a string query, searches Twitter for Tweets containing that word
# and returns overall sentiment and a tweet that contains the query
def search_twitter(query):
    # This handles Twitter authentification
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth_handler=auth)
    search_results = api.search(query)

    threshold = 0
    pos_sent_tweet = 0
    neg_sent_tweet = 0
    sentiment = 'Unknown'
    for tweet in search_results:
        analysis = TextBlob(tweet.text)
        if analysis.sentiment.polarity >= threshold:
            pos_sent_tweet = pos_sent_tweet + 1
        else:
            neg_sent_tweet = neg_sent_tweet + 1
    if pos_sent_tweet > neg_sent_tweet:
        sentiment = 'Positive'
    else:
        sentiment = 'Negative'

    for result in search_results:
        id_str = result._json['id_str']
        raw_html = api.get_oembed(id_str)['html']
        embed_html = raw_html.split('<script')[0]
        return sentiment, embed_html
