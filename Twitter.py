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

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        for url in tweet["entities"]["urls"]:
            print (" - found URL: %s" % url["expanded_url"])
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth_handler=auth)
    search_results = api.search("MSFT")
    for result in search_results:
        print(result)

    #stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keyword: '#NFL'
    #stream.filter(track=[ 'American Airlines' ])
