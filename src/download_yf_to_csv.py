import yfinance as yf
import os

def download_stock_data(ticker: str, start_date: str, end_date: str, file_dir: str = "../data") -> 'pandas.DataFrame':
    # Fetch historical market data
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    # Define file path
    file_path = os.path.join(file_dir, f"{ticker}_data.csv")

    # Write data to CSV file
    stock_data.to_csv(file_path)

    # Display first few rows
    print(stock_data.head())

    # print length of data
    print(f"Data length: {len(stock_data)}")

    return stock_data

if __name__ == "__main__":
    # read input from user
    ticker = input("Enter stock ticker: ")

    download_stock_data(ticker, "2023-01-01", "2025-12-31")

