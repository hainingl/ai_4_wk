import yfinance as yf
import os

# Define stock tickers
ticker = "^HSI"  # Example: Hang Seng Index
ticker = "MCHI"  # Example: Hang Seng Index

# Fetch historical market data
stock_data = yf.download(ticker, start="2023-01-01", end="2025-12-31")

# Define file path
file_path = os.path.join("../data", f"{ticker}_2023.csv")

# Write data to CSV file
stock_data.to_csv(file_path)

# Display first few rows
print(stock_data.head())
