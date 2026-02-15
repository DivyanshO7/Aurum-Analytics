import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import datetime as dt

def train_predict_model(df):
    """
    Trains a Linear Regression model on historical gold data.
    Predicts the next day's price and 7-day trend.
    """
    if df.empty:
        return None

    # Prepare Data for Training
    # We will use 'Date' converted to ordinal as the feature
    df['Date_Ordinal'] = df['Date'].map(dt.datetime.toordinal)
    
    X = df[['Date_Ordinal']]
    y = df['Price']
    
    # Train Model (Using all data for this simple prototype to predict future)
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict Next Day
    last_date = df['Date'].iloc[-1]
    next_date = last_date + dt.timedelta(days=1)
    next_date_ordinal = np.array([[next_date.toordinal()]])
    
    next_price = model.predict(next_date_ordinal)[0]
    
    # Predict 7 Days Trend
    future_dates = [last_date + dt.timedelta(days=i) for i in range(1, 8)]
    future_ordinals = np.array([[d.toordinal()] for d in future_dates])
    future_prices = model.predict(future_ordinals)
    
    # Determine Trend Direction
    trend_slope = model.coef_[0]
    
    if trend_slope > 0.5:
        trend = "Bullish"
    elif trend_slope < -0.5:
        trend = "Bearish"
    else:
        trend = "Neutral"
        
    return {
        "next_price": round(next_price, 2),
        "trend": trend,
        "future_dates": [d.strftime('%Y-%m-%d') for d in future_dates],
        "future_prices": [round(p, 2) for p in future_prices],
        "slope": trend_slope
    }
