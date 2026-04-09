from flask import Flask, render_template, jsonify, request, redirect
from fetch_data import get_gold_data
from sentiment import get_news_sentiment
from model import train_predict_model
import pandas as pd
import json

app = Flask(__name__)

# Global Cache (Simple in-memory)
cache = {
    "gold_data": None,
    "sentiment": None,
    "prediction": None,
    "api_status": {
        "gold": "Unknown",
        "news": "Unknown"
    }
}

def refresh_data():
    """
    Refreshes data from sources. 
    In a production app, this would be a background task.
    """
    print("Refreshing Data...")
    
    # 1. Fetch Gold Data
    df = get_gold_data(period='1y')
    cache['gold_data'] = df
    if df.empty:
        cache['api_status']['gold'] = 'Failed'
    else:
        cache['api_status']['gold'] = 'Connected'
    
    # 2. Get Sentiment
    sent = get_news_sentiment()
    cache['sentiment'] = sent
    cache['api_status']['news'] = sent.get('api_status', 'Unknown')
    
    # 3. Predict Fusion
    if not df.empty:
        sent_score = cache['sentiment']['average_score'] if cache['sentiment'] else 0
        pred = train_predict_model(df, sent_score)
        cache['prediction'] = pred

# Initial Load
refresh_data()

@app.route('/')
def home():
    # Ensure data is loaded
    if cache['gold_data'] is None:
        refresh_data()
        
    # Get latest price
    latest_price = 0
    if cache['gold_data'] is not None and not cache['gold_data'].empty:
        latest_price = round(cache['gold_data'].iloc[-1]['Price'], 2)
        
    return render_template('index.html', 
                           price=latest_price,
                           prediction=cache['prediction'],
                           sentiment=cache['sentiment'],
                           system_status=cache['api_status'],
                           page='home')

@app.route('/news')
def news():
    if cache['sentiment'] is None:
        refresh_data()
    return render_template('news.html', 
                           news=cache['sentiment']['articles'],
                           page='news')

@app.route('/chart')
def chart():
    return render_template('chart.html', page='chart')

@app.route('/prediction')
def prediction():
    if cache['prediction'] is None:
        refresh_data()
        
    return render_template('prediction.html', 
                           prediction=cache['prediction'],
                           sentiment=cache['sentiment'],
                           page='prediction')

@app.route('/api/chart-data')
def chart_data():
    if cache['gold_data'] is None:
        refresh_data()
        
    df = cache['gold_data']
    
    # Convert dates to string
    dates = df['Date'].dt.strftime('%Y-%m-%d').tolist()
    prices = df['Price'].tolist()
    
    return jsonify({
        'dates': dates,
        'prices': prices,
        'prediction': cache['prediction']
    })

@app.route('/refresh', methods=['POST'])
def refresh():
    # Force news to increment its manual refresh counter
    sent = get_news_sentiment(force_refresh=True)
    cache['sentiment'] = sent
    cache['api_status']['news'] = sent.get('api_status', 'Unknown')
    
    # Repredict Fusion with new sentiment score so the UI updates
    if cache['gold_data'] is not None and not cache['gold_data'].empty:
        pred = train_predict_model(cache['gold_data'], sent.get('average_score', 0))
        cache['prediction'] = pred
        
    return redirect(request.form.get('next', '/'))

if __name__ == '__main__':
    app.run(debug=True)
