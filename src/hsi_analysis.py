import pandas as pd

# Load the CSV file, skipping first 2 rows and using 3rd row as header
df = pd.read_csv('../data/^HSI_2023.csv', skiprows=2, header=0)

# Print the columns to debug
print("Columns in the DataFrame:", df.columns)

# Print the first few rows to inspect the structure
print("First few rows of the DataFrame:")
print(df.head())

# Parse dates from first column
df['Date'] = pd.to_datetime(df.iloc[:, 0])

# Calculate daily percentage changes for Close prices
if 'Close' in df.columns:
    df['Pct_Change'] = df['Close'].pct_change() * 100
else:
    print("Error: 'Close' column not found in the DataFrame")

# Save results to new CSV
df.to_csv('hsi_analysis_results.csv', index=False)

print("Analysis complete. Results saved to hsi_analysis_results.csv")