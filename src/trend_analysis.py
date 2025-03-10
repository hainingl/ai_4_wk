# need to find large cap stock in US which has upward trend in the past 5 days
# and has a good potential to grow in the future
# 1. find large cap stock
# 2. find stock with upward trend in the past 5 days
# 3. find stock with good potential to grow in the future

import requests
import json
import pandas as pd
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load all stock data from ../data folder
import os
import glob

def get_top_trending_stocks(num_stocks: int = 5) -> pd.DataFrame:
    all_files = glob.glob('../data/*.csv')
    df_list = []

    for filename in all_files:
        symbol = os.path.basename(filename).split('.')[0]
        temp_df = pd.read_csv(filename, on_bad_lines='skip')
        temp_df['Symbol'] = symbol
        df_list.append(temp_df)

    df = pd.concat(df_list)
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')

    # Convert relevant columns to numeric types
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

    # Calculate 5-day trends
    df['5_day_change'] = df.groupby('Symbol')['Close'].pct_change(5)

    # Get latest 5-day change for each stock
    latest_trends = df.groupby('Symbol')['5_day_change'].last().sort_values(ascending=False)

    # Print top trending stocks
    print(f"Top {num_stocks} Trending Stocks:")
    print(latest_trends.head(num_stocks))

    return latest_trends.head(num_stocks)


# Call the function and save results
top_trending_stocks = get_top_trending_stocks(num_stocks=10)

# Plot the chart for the top trending stocks
for symbol in top_trending_stocks.index:
    stock_data = pd.read_csv(f'../data/{symbol}.csv', on_bad_lines='skip')
    stock_data['Date'] = pd.to_datetime(stock_data['Date'], format='mixed')
    stock_data['Close'] = pd.to_numeric(stock_data['Close'], errors='coerce')

    plt.figure(figsize=(10, 5))
    plt.plot(stock_data['Date'], stock_data['Close'], label=symbol)
    plt.title(f'{symbol} Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'../data/{symbol}_trend.png')
    plt.show()

top_trending_stocks.to_csv('../data/top_trending_stocks.csv')
print("Top trending stocks saved to top_trending_stocks.csv")
top_trending_stocks.to_csv('../data/top_trending_stocks.csv')
print("Top trending stocks saved to top_trending_stocks.csv")

# Save results
print("Top trending stocks saved to top_trending_stocks.csv")