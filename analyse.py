from fetch import get_senticrypt_data

def analyse_data():
    sentiment_data = get_senticrypt_data()

    if not sentiment_data or len(sentiment_data) < 2:
        print("Data currently unavailable — try again later.")
        return

    latest_sentiment = sentiment_data[-1]
    previous_sentiment = sentiment_data[-2]

    price_today = latest_sentiment['price']
    sentiment_today = latest_sentiment['mean']
    sentiment_yesterday = previous_sentiment['mean']

    # Prediction based on yesterday's sentiment
    prediction = "FLAT"
    if sentiment_yesterday > 0.1:
        prediction = "UP"
    elif sentiment_yesterday < -0.1:
        prediction = "DOWN"

    # We can't calculate a "hit" without actual price movement data.
    # We will just display the prediction.
    
    # Scale sentiment for display
    scaled_sentiment = (sentiment_today + 1) * 50

    print(f"           BTC price: ${price_today:,.2f}")
    print(f"Sentiment (0-100): {scaled_sentiment:.2f}")
    print(f"Yesterday’s prediction: {prediction}")

if __name__ == "__main__":
    analyse_data()