import pandas as pd
import pyodbc
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

# Azure SQL Connection
conn_str = os.getenv("SQL_ODBC_CONNECTION_STRING")

try:
    # Read all stock file paths
    with open("latest_files.txt", "r") as f:
        FILE_PATHS = [line.strip() for line in f.readlines()]

    if not FILE_PATHS:
        raise FileNotFoundError("❌ No stock files found!")

    # Connect to Azure SQL
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.fast_executemany = True  # Optimize bulk inserts

    # Define valid ETF tables
    valid_etfs = {"SPY", "QQQ", "DIA", "IWM"}

    for file_path in FILE_PATHS:
        if not os.path.exists(file_path):
            print(f"⚠️ Skipping missing file: {file_path}")
            continue

        print(f"📥 Processing {file_path}...")

        try:
            # Read CSV into DataFrame
            df = pd.read_csv(file_path)

            # Ensure expected columns exist
            required_columns = {"Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"}
            if not required_columns.issubset(set(df.columns)):
                print(f"❌ Skipping {file_path}: Missing required columns!")
                continue

            # Convert Date column
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

            # Drop rows with invalid dates
            df = df.dropna(subset=["Date"])

            # Rename columns for SQL compatibility
            df.rename(columns={"Adj Close": "Adj_Close"}, inplace=True)

            # Extract ETF name from filename
            etf_name = os.path.basename(file_path).split("_")[0]

            # Ensure ETF is valid
            if etf_name not in valid_etfs:
                print(f"⚠️ Skipping {file_path}: ETF name '{etf_name}' is not recognized.")
                continue

            sql_table = f"{etf_name}_StockPrices"  # Map to correct SQL table

            print(f"🔹 Inserting data into {sql_table}...")

            # Convert DataFrame to tuples for SQL insertion
            data_tuples = list(df[["Date", "Open", "High", "Low", "Close", "Adj_Close", "Volume"]].itertuples(index=False, name=None))

            if not data_tuples:
                print(f"⚠️ No valid data to insert for {file_path}. Skipping.")
                continue

            # Insert data into the respective SQL table
            cursor.executemany(f"""
                INSERT INTO {sql_table} (Date, [Open], High, Low, [Close], Adj_Close, Volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, data_tuples)

            conn.commit()
            print(f"✅ Uploaded {file_path} to {sql_table} successfully.")

        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")

    # Close connection
    cursor.close()
    conn.close()

    print("🎉 All stock files uploaded successfully!")

except Exception as e:
    print(f"❌ Fatal error inserting stock data into SQL: {e}")
    sys.exit(1)