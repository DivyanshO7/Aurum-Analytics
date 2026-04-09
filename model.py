import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import datetime as dt

def train_predict_model(df, sentiment_score=0):
    """
    Trains a Linear Regression model on historical gold data.
    Predicts the next day's price and 7-day trend using Econometric fusion.
    """
    if df.empty:
        return None

    # Prepare Data for Training
    df['Date_Ordinal'] = df['Date'].map(dt.datetime.toordinal)
    X = df[['Date_Ordinal']]
    y = df['Price']
    
    # Train Model to get Baseline Momentum (Drift)
    model = LinearRegression()
    model.fit(X, y)
    
    slope = model.coef_[0]
    last_price = df['Price'].iloc[-1]
    last_date = df['Date'].iloc[-1]
    std_dev = df['Price'].diff().std()
    
    # 7 Days Trend Fusion Generation (Random Walk with Drift)
    future_dates = [last_date + dt.timedelta(days=i) for i in range(1, 8)]
    future_prices = []
    daily_trends = []
    
    current_price = last_price
    # Seed randomly using the last date so the deterministic shape holds during the day
    np.random.seed(int(last_date.timestamp()) if hasattr(last_date, 'timestamp') else last_date.toordinal())
    
    for i in range(1, 8):
        # We decay the news sentiment impact slightly over the future days
        decayed_sentiment_impact = (sentiment_score * std_dev) * (1 / i)
        
        # Remove noise exclusively for day 1 so the UI visual math sums perfectly without hidden variance
        noise = 0 if i == 1 else np.random.normal(0, std_dev * 0.2)
        
        daily_movement = slope + decayed_sentiment_impact + noise
        current_price += daily_movement
        future_prices.append(current_price)
        
        if daily_movement > std_dev * 0.1:
            daily_trends.append("Bullish")
        elif daily_movement < -(std_dev * 0.1):
            daily_trends.append("Bearish")
        else:
            daily_trends.append("Stable")
            
    np.random.seed()
    
    # Sync Day 1 Fusion stats tightly to future_prices[0] to prevent mismatch
    next_price = future_prices[0]
    # Re-derive exact noise included so breakdown math is perfect:
    net_change_day_1 = next_price - last_price
    graph_base_change = slope
    news_impact_change = sentiment_score * std_dev
    
    # Determine Overall 7-Day Trend Direction
    price_change = future_prices[-1] - last_price
    percent_change = (price_change / last_price) * 100
    
    if percent_change > 0.1:
        overall_trend = "Bullish"
    elif percent_change < -0.1:
        overall_trend = "Bearish"
    else:
        overall_trend = "Neutral"

    return {
        "next_price": round(next_price, 2),
        "trend": overall_trend,
        "future_dates": [d.strftime('%Y-%m-%d') for d in future_dates],
        "future_prices": [round(p, 2) for p in future_prices],
        "daily_trends": daily_trends,
        "slope": round(percent_change, 3),
        "breakdown": {
            "graph_base_change": round(graph_base_change, 2),
            "news_impact_change": round(news_impact_change, 2),
            "net_change_day_1": round(net_change_day_1, 2)
        }
    }
