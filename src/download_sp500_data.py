import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_sp500_tickers():
    """Get list of S&P 500 tickers"""
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    return sp500['Symbol'].tolist()

def download_sp500_data(days=5):
    """Download historical data for all S&P 500 components"""
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days+7)).strftime('%Y-%m-%d')  # Extra buffer
    
    tickers = get_sp500_tickers()
    
    for ticker in tickers:
        try:
            # Download data with volume
            data = yf.download(ticker, start=start_date, end=end_date)
            if not data.empty:
                # Save to CSV
                data.to_csv(f'../data/{ticker}.csv')
                print(f"Downloaded {ticker}")
            else:
                print(f"No data for {ticker}")
        except Exception as e:
            print(f"Error downloading {ticker}: {str(e)}")

if __name__ == "__main__":
    download_sp500_data()
