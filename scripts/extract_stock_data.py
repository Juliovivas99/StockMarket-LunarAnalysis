import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# Define ETFs for the major indices
etfs = {
    "SPY": "S&P 500",
    "QQQ": "NASDAQ",
    "DIA": "Dow Jones",
    "IWM": "Russell 2000"  
}

# Define date range (5 years back)
START_DATE = (datetime.today().replace(year=datetime.today().year - 5)).strftime('%Y-%m-%d')
END_DATE = datetime.today().strftime('%Y-%m-%d')

# Ensure output directory exists
os.makedirs("data", exist_ok=True)

# Store latest file paths
latest_files = []

for etf, index_name in etfs.items():
    try:
        print(f"📥 Fetching data for {index_name} ({etf})...")

        # Fetch data from Yahoo Finance
        data = yf.download(etf, start=START_DATE, end=END_DATE, auto_adjust=False)

        # Reset index to make "Date" a column
        data.reset_index(inplace=True)

        # Remove any empty rows
        data = data[data["Date"].notna()]

        # Define a separate CSV file for each ETF
        output_file = f"data/{etf}_stock_{END_DATE}.csv"
        data.to_csv(output_file, index=False)

        # Store the latest file path for tracking
        latest_files.append(output_file)

        print(f"✅ Saved {index_name} data to: {output_file}")

    except Exception as e:
        print(f"❌ Error fetching data for {index_name} ({etf}): {e}")

# Save all latest file paths in a reference file
with open("latest_files.txt", "w") as f:
    for file in latest_files:
        f.write(file + "\n")

print("✅ All ETF data exported successfully!")