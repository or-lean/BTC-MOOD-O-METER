from flask import Flask, render_template, jsonify
from fetch import get_senticrypt_data

app = Flask(__name__)

def get_latest_data():
    sentiment_data = get_senticrypt_data()

    if not sentiment_data or len(sentiment_data) < 2:
        return None

    # Get the last two entries for today and yesterday's sentiment
    latest_sentiment = sentiment_data[-1]
    previous_sentiment = sentiment_data[-2]

    sentiment_today = latest_sentiment['mean']
    sentiment_yesterday = previous_sentiment['mean']

    # For this example, we'll use the sentiment score directly.
    # A score > 0 might suggest positive sentiment, < 0 negative.
    # The 'fng' value in the old code was 0-100, so we'll scale the sentiment
    # from -1 to 1 to a 0-100 range for the gauge.
    # Scaled value = (sentiment + 1) * 50
    gauge_value = (sentiment_today + 1) * 50

    # We'll need a proxy for price movement. Let's assume for this PoC
    # that a significant increase in sentiment suggests an "UP" market movement.
    prediction = "FLAT"
    if sentiment_yesterday > 0.1: # Threshold for "UP" prediction
        prediction = "UP"
    elif sentiment_yesterday < -0.1: # Threshold for "DOWN" prediction
        prediction = "DOWN"

    # Since we don't have real price data, we can't calculate a "hit".
    # We can simulate it or just display the prediction.
    # For this version, we'll just show the prediction and sentiment.
    # We'll also need a value for price_usd for the template.
    # We can use the BTC price from the sentiment data.
    price_today = latest_sentiment['price']


    return {
        "price_usd": price_today,
        "fng": gauge_value, # This is now our scaled sentiment
        "prediction": prediction,
        "hit": False # Cannot be calculated anymore
    }

@app.route("/")
def home():
    data = get_latest_data()
    if data is None:
        return "Data currently unavailable — try again later.", 503
    return render_template("index.html", **data)

@app.route("/api/latest")
def api_latest():
    data = get_latest_data()
    if data is None:
        return jsonify({"error": "Data currently unavailable"}), 503
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
