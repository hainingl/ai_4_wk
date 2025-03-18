import os
import glob
import time
import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import webbrowser
from typing import List
from datetime import datetime, timedelta

# Define the URL templates as global variables
DIVIDEND_URL_TEMPLATE = 'https://q.stock.sohu.com/cn/{symbol}/fhsp.shtml'
FUND_URL_TEMPLATE = 'https://fundf10.eastmoney.com/jdzf_{symbol}.html'
CHART_CHINA_ONE_DAY_TEMPLATE = 'https://j4.dfcfw.com/charts/pic6/{symbol}.png?v={date_second}'
CHART_US_TEMPLATE = 'https://stockcharts.com/c-sc/sc?s={symbol}&p=D&b=5&i=t4273131773c'

# TradingView URLs
CHART_TRADING_VIEW_TEMPLATE = 'https://cn.tradingview.com/chart/T3FsDPIK/?symbol={symbol}'
LAYOUT_HOUR_DAY = 'https://cn.tradingview.com/chart/mGKyRfcA/?symbol={symbol}'
# LAYOUT_MIN_HOUR = 'https://cn.tradingview.com/chart/ezkzlG7W/?symbol={symbol}'

CN_FUND_SCREEN = 'https://cn.tradingview.com/chart/0cdJ1j31/?symbol={symbol}'

# make it parameterized
DAILY_BUYING_SCREEN_TEMPLATE='https://cn.tradingview.com/chart/ezkzlG7W/?symbol={symbol}'

SCREEN_TEMPLATE ='https://cn.tradingview.com/chart/T3FsDPIK/?symbol={symbol}&interval={interval}'
SYMBOL_INTERVAL_SCREEN_TEMPLATE ='https://cn.tradingview.com/chart/SWCnHzWx/?symbol={symbol}&interval={interval}'

import pprint

from typing import List

LAYOUTS = {
    "Multi": {
        "1H_1D": "https://cn.tradingview.com/chart/gcIkMrqM/",
        "Daily_Buying": "https://cn.tradingview.com/chart/ezkzlG7W/",
    },
    "One": {
        "多-中ETF-30m": "https://cn.tradingview.com/chart/OzpPEC1I/",
        "Fixed_start_one_screen": "https://cn.tradingview.com/chart/DWv74HO8/",
    }
}
# create function to print out value by name on the bottom level
def get_layout_by_name(layouts: dict = LAYOUTS, name: str = None, multi: bool = True) -> List[str]:
    values = []
    if name is None:
        if multi:
            for k, v in layouts['Multi'].items():
                # print(f"{k}: {v}")
                values.append(v)
        else:
            for k, v in layouts['One'].items():
                # print(f"{k}: {v}")
                values.append(v)
    else:
        for k, v in layouts.items():
            if isinstance(v, dict):
                values.extend(get_layout_by_name(v, name, multi))
            else:
                if name in k:
                    # print(f"{k}: {v}")
                    values.append(v)
    return values

def create_top_trending_stocks_dict(top_trending_stocks):
    return {
        stock: {
            "symbol": stock,
            "interval": "1H",
            "layout": "vZjXf8fw"
        } for stock in top_trending_stocks
    }


def display_charts_from_dict(stock_dict):
    for key, value in stock_dict.items():
        symbol = value['symbol']
        url = SCREEN_TEMPLATE.format(layout=value['layout'], symbol=symbol, interval=value['interval'])
        display_chart_in_browser([symbol], url)

import webbrowser

def show_stock_by_algo(stock, layout_name="1H_1D"):
    algos = get_layout_by_name(LAYOUTS, layout_name)
    # create loops over algos
    for algo in algos:
        url = algo + '?symbol=' + stock
        try:
            browser = webbrowser.get('TV_STOCKS')
        except webbrowser.Error:
            browser = webbrowser.get()
        browser.open(url)
        
def display_chart_in_browser(symbols: List[str], url_template: str = CHART_US_TEMPLATE) -> None:
    """
    Displays URLs for stock symbols in a web browser.

    Parameters:
    symbols (List[str]): A list of stock symbols.
    url_template (str): The URL template to use for displaying stock URLs.

    Returns:
    None
    """
    # if symbols is empty, return
    if not symbols:
        return  
    
    for symbol in symbols:
        try:
            url = url_template.format(symbol=symbol)
            print(f"Opening URL: {url}")
            try:
                browser = webbrowser.get('TV_STOCKS')
            except webbrowser.Error:
                browser = webbrowser.get()
            browser.open(url)
        except webbrowser.Error as e:
            print(f"Failed to open URL for symbol {symbol} in 'TV_STOCKS' browser: {e}")
        except Exception as e:
            print(f"An unexpected error occurred for symbol {symbol}: {e}")

def get_top_trending_stocks(num_stocks: int = 5) -> list:
    # find current path and print it
    print(os.getcwd())
    
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

    return latest_trends.head(num_stocks).index.tolist()

def plot_top_trending_stocks(stock_symbols: List[str]) -> None:
    for symbol in stock_symbols:
        filename = f'{symbol}.csv'
        stock_data = pd.read_csv(f'../data/{filename}', on_bad_lines='skip')
        
        # Skip the first 3 rows and reset the header
        stock_data = stock_data.iloc[3:].reset_index(drop=True)
        stock_data.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']

        # Print the columns to debug
        print(f"Columns in {filename}: {stock_data.columns}")

        if 'Date' in stock_data.columns and 'Close' in stock_data.columns:
            stock_data['Date'] = pd.to_datetime(stock_data['Date'], format='mixed')
            stock_data['Close'] = pd.to_numeric(stock_data['Close'], errors='coerce')

            # Calculate percentage increase
            stock_data['Pct_Change'] = stock_data['Close'].pct_change() * 100

            fig, ax1 = plt.subplots(figsize=(10, 5))

            ax1.plot(stock_data['Date'], stock_data['Close'], label=f'{symbol} Close Price', color='blue')
            ax1.set_xlabel('Date', fontweight='bold')
            ax1.set_ylabel('Close Price', color='blue')
            ax1.tick_params(axis='y', labelcolor='blue')
            ax1.legend(loc='upper left')
            ax1.grid(True)
            ax1.xaxis.set_major_locator(mdates.MonthLocator())
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.xticks(rotation=45, fontweight='bold')

            ax2 = ax1.twinx()
            ax2.plot(stock_data['Date'], stock_data['Pct_Change'], label=f'{symbol} % Change', color='orange')
            ax2.set_ylabel('Percentage Change', color='orange')
            ax2.tick_params(axis='y', labelcolor='orange')
            ax2.legend(loc='upper right')

            # Add y=0 line
            ax2.axhline(y=0, color='black', linewidth=2, linestyle='--')

            # Add big red star for volatile days
            volatile_days = stock_data[abs(stock_data['Pct_Change']) > 10]
            ax2.scatter(volatile_days['Date'], volatile_days['Pct_Change'], color='red', s=100, marker='*', label='Volatile Day')
            for idx, row in volatile_days.iterrows():
                ax2.text(row['Date'], row['Pct_Change'], 'Volatile', color='red', fontsize=12, fontweight='bold')

            plt.title(f'{symbol} Stock Price and Percentage Change')
            plt.tight_layout()
            plt.savefig(f'../data/{symbol}_trend_pct_change.png')
            plt.show()
        else:
            print(f"Skipping {symbol} as it does not contain 'Date' or 'Close' column")

from typing import List
from IPython.display import display, HTML

def display_tradingview_iframes(symbols: List[str], interval: str = '10') -> None:
    """
    Display TradingView iframes for a list of symbols in a table format.

    Parameters:
    symbols (List[str]): List of stock symbols to display.
    interval (str): Time interval for the TradingView chart. Default is '10'.
    """
    iframe_template = """
    <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_{symbol}&symbol={symbol}&interval={interval}&hidesidetoolbar=1&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=[%22MACD@tv-basicstudies%22]&theme=Light&style=1&timezone=Etc%2FUTC&withdateranges=1&hideideas=1&studies_overrides={{}}&overrides={{}}&enabled_features=[]&disabled_features=[]&locale=en&utm_source=tradingview.com&utm_medium=widget_new&utm_campaign=symbol-overview" width="700" height="400" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
    """
    
    rows = []
    for i in range(0, len(symbols), 2):
        row_symbols = symbols[i:i+2]
        row_iframes = "".join([iframe_template.format(symbol=symbol, interval=interval) for symbol in row_symbols])
        rows.append(f"<tr>{row_iframes}</tr>")
    
    table_html = f"<table>{''.join(rows)}</table>"
    display(HTML(table_html))
