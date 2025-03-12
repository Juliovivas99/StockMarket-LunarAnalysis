import pandas as pd
import pyodbc
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

# Azure SQL Connection
conn_str = os.getenv("SQL_ODBC_CONNECTION_STRING")

# Batch size for inserting data in chunks
BATCH_SIZE = 500

try:
    # Read lunar data CSV
    CSV_FILE = "data/lunar_phases.csv"

    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(f"❌ File {CSV_FILE} not found!")

    print(f"📥 Processing {CSV_FILE}...")

    # Read CSV into DataFrame
    df = pd.read_csv(CSV_FILE)

    # Ensure required columns exist
    if "Date" not in df.columns or "Phase" not in df.columns:
        raise ValueError("❌ CSV file missing required columns: 'Date' and 'Phase'.")

    # Convert "Date" column to datetime
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

    # Drop rows with invalid dates
    df = df.dropna(subset=["Date"])

    # Convert DataFrame to a list of tuples
    data_tuples = list(df.itertuples(index=False, name=None))

    if not data_tuples:
        raise ValueError("❌ No valid data to insert. Check CSV contents.")

    # Connect to Azure SQL
    print("🔗 Connecting to SQL Server...")
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.fast_executemany = True  # Enable fast bulk inserts

    print(f"🔹 Preparing to insert {len(data_tuples)} rows into LunarPhases table...")

    # Insert data in batches to prevent timeout issues
    for i in range(0, len(data_tuples), BATCH_SIZE):
        batch = data_tuples[i:i + BATCH_SIZE]
        print(f"📤 Inserting batch {i // BATCH_SIZE + 1} ({len(batch)} rows)...")

        cursor.executemany("""
            INSERT INTO LunarPhases (Date, Phase) VALUES (?, ?)
        """, batch)

        conn.commit()

    # Close connection
    cursor.close()
    conn.close()

    print(f"✅ Successfully uploaded {len(data_tuples)} lunar phase records to Azure SQL.")

except Exception as e:
    print(f"❌ Error inserting lunar phases into SQL: {e}")
    sys.exit(1)