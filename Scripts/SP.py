#Alpha Vantage! Your API key is: AR7YDO4OYCHEAZBA
import tweepy
import numpy as np
import requests
import json
import matplotlib.pyplot as plt
from textblob import TextBlob
from sklearn.svm import SVR
plt.switch_backend('TkAgg')
consumer_key= 'mupucnuirYgcDUcdoWnbKI5Sj'
consumer_secret= 'bOkWp3ysvnlr3Zw9bzFNPTVK0TijLSbFaU9MKrWUZSRJ9wIxLN'
access_token='812697466990641152-qO3nshDugAhzCu2e8wihgUYnc5ricqC'
access_token_secret='edXnxrMcjJOJgS8biXrAprAxUCNM5nhiUJUT7C3dsac2U'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
dates = []
prices = []
input_CN = input()
input_Date = input_CN.split(' ')[1]
input_CN = input_CN.split(' ')[0]
public_tweets = api.search('Google')

threshold=0
pos_sent_tweet=0
neg_sent_tweet=0
for tweet in public_tweets:
    analysis=TextBlob(tweet.text)
    if analysis.sentiment.polarity>=threshold:
        pos_sent_tweet=pos_sent_tweet+1
    else:
        neg_sent_tweet=neg_sent_tweet+1
if pos_sent_tweet>neg_sent_tweet:
    print ("Overall Pos")
else:
    print ("Overall Neg")

def predict_prices(dates,prices,x):
    r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+str(input_CN)+'&apikey=AR7YDO4OYCHEAZBA')
    response_dict = r.json()
    response_dict_improved = response_dict["Time Series (Daily)"]
    for var in response_dict_improved:
        price_json = response_dict_improved.get(var).get('1. open')
        dates.append((int(var.split('-')[1])*31)+int(var.split('-')[2]))
        prices.append(price_json)
    dates = np.reshape(dates,(-1, 1))
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    svr_rbf.fit(dates, prices)
    plt.scatter(dates, prices, color='orange', label='Data')
    plt.plot(dates, svr_rbf.predict(dates), color='red', label='RBF model')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Company Stock')
    plt.legend()
    plt.show()
    return svr_rbf.predict([[x]])[0]

#predicted_price = predict_prices(dates, prices, 14)

print (predict_prices(dates,prices,input_Date))# the number is the date of which you wanna predict
