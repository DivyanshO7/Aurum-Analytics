import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_gold_data(period='1y'):
    """
    Fetches historical gold price data from yfinance.
    Ticker: GC=F (Gold Futures)
    """
    try:
        # Gold Futures Ticker
        ticker = "GC=F"
        
        # Fetch data
        gold_data = yf.download(ticker, period=period, interval='1d', progress=False)
        
        # Reset index to make Date a column
        gold_data.reset_index(inplace=True)
        
        # Select relevant columns
        df = gold_data[['Date', 'Close']]
        
        # Renaissance yfinance might return MultiIndex columns, flatten if necessary
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        # Rename columns for consistency
        df = df.rename(columns={'Close': 'Price'})
        
        # Ensure Date is datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Drop any missing values
        df.dropna(inplace=True)
        
        # Sort by Date
        df.sort_values('Date', inplace=True)
        
        return df

    except Exception as e:
        print(f"Error fetching gold data: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    # Test the function
    df = get_gold_data()
    print(df.head())
    print(df.tail())
