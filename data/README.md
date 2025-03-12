# Data Directory

This directory contains data files for the Stock Market & Lunar Phase Analysis project.

## Directory Structure

```
data/
├── raw/           # Raw data extracted from sources
└── processed/     # Processed data ready for analysis
```

## Data Files

### Stock Data

Stock price data for major ETFs, including:

- SPY_stock_YYYY-MM-DD.csv - S&P 500 ETF
- QQQ_stock_YYYY-MM-DD.csv - Nasdaq 100 ETF
- DIA_stock_YYYY-MM-DD.csv - Dow 30 ETF
- IWM_stock_YYYY-MM-DD.csv - Russell 2000 ETF

Each stock data file contains the following columns:

- Date: Trading date
- Open: Opening price
- High: Highest price during the day
- Low: Lowest price during the day
- Close: Closing price
- Volume: Trading volume
- Adj Close: Adjusted closing price

### Lunar Phase Data

`lunar_phases.csv` - Contains lunar phase data with columns:

- Date: Calendar date
- Phase: Lunar phase (New Moon, Waxing Crescent, First Quarter, etc.)
- PhaseAngle: Precise lunar phase angle in degrees

## Data Sources

- Stock data is sourced from Yahoo Finance API
- Lunar phase data is sourced from NASA API

## Data Flow

1. Raw data is extracted using Python scripts in the `scripts/` directory
2. Data is uploaded to Azure Blob Storage for persistent storage
3. Data is then loaded into an Azure SQL Database for analysis
4. Analysis scripts join stock data with lunar phases on the date

## Notes

- Data files are timestamped with the extraction date
- New data can be added by running the extraction scripts again
- Historical data is preserved for longitudinal analysis
