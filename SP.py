import tweepy
import csv
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
from sklearn.svm import SVR
plt.switch_backend('TkAgg')
consumer_key= 'mupucnuirYgcDUcdoWnbKI5Sj'
consumer_secret= 'bOkWp3ysvnlr3Zw9bzFNPTVK0TijLSbFaU9MKrWUZSRJ9wIxLN'
access_token='812697466990641152-nYSiwMkz62iY61s9s5hnngO1s1xOD1h'
access_token_secret='fPx4r3x9Uegt1vaA8sIEg7DaFHJUEPkZvtulNwDvmGMHF'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

public_tweets = api.search('American Airlines')
print (public_tweets[2].text)

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

dates = []
prices = []
def get_data(filename):
    with open(filename, 'r') as csvfile:
        csv_file_reader = csv.reader(csvfile)
        next(csv_file_reader)
        for row in csv_file_reader:
            dates.append(int(row[0].split('-')[2]))
            prices.append(float(row[1]))
    return

def predict_prices(dates, prices, x):
    dates = np.reshape(dates,(-1, 1))
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    svr_rbf.fit(dates, prices)
    plt.scatter(dates, prices, color='orange', label='Data')
    plt.plot(dates, svr_rbf.predict(dates), color='red', label='RBF model')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('American Airlines Stock')
    plt.legend()
    return svr_rbf.predict([[x]])[0]
    plt.show()
get_data('AAL.csv')

#predicted_price = predict_prices(dates, prices, 14)

print (predict_prices(dates, prices,12))# the number is the date of which you wanna predict
