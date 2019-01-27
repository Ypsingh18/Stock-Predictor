from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from SP import predict_prices, date_to_int
from Twitter import search_twitter

app = Flask(__name__)
CORS(app)

KNOWN_COMPANIES = {
    'AAPL': 'Apple',
    'MSFT': 'Microsoft',
    'GOOG': 'Google',
    'FB': 'Facebook',
    'COF': 'Capital One',
    'ATVI': 'Activision'
}


@app.route('/')
def index():
    return 'Hello world!'


@app.route('/predict/<string:symbol>/<string:date>', methods=['GET'])
def predict(symbol, date):
    predicted_price, (xs, ys) = predict_prices(symbol, date_to_int(date))
    tweet = ''
    sentiment = 'Unknown'
    if symbol.upper() in KNOWN_COMPANIES:
        sentiment, tweet = search_twitter(KNOWN_COMPANIES[symbol.upper()])
    else:
        sentiment, tweet = search_twitter(symbol)
    return jsonify({'price': predicted_price, 'xs': xs.tolist(), 'ys': ys, 'tweet': tweet, 'sentiment': sentiment})


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        f = request.files['face_image']
        print('face_images/' + request.args.get('username') + '.jpg')
        f.save('face_images/'+request.args.get('username')+'.jpg')


if __name__ == '__main__':
    app.run(debug=True)
