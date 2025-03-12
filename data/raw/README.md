# Raw Data Directory

This directory is intended to store raw, unprocessed data files extracted directly from source systems.

## Expected Contents

- Raw stock price data from Yahoo Finance API
- Raw lunar phase data from NASA API
- Any other source data before processing

## Data Extraction Process

The raw data files are extracted using the following scripts:

- `scripts/extract_stock_data.py` - Extracts stock price data for SPY, QQQ, DIA, and IWM from Yahoo Finance
- `scripts/extract_moon_data.py` - Extracts lunar phase data from NASA's API

## Data Format

Each raw data file follows a specific format:

### Stock Data Files

- CSV format
- Headers: Date, Open, High, Low, Close, Adj Close, Volume
- Daily price and volume data

### Lunar Phase Data

- CSV format
- Headers: Date, Phase, Illumination
- Phase values: New Moon, Waxing Crescent, First Quarter, Waxing Gibbous, Full Moon, Waning Gibbous, Last Quarter, Waning Crescent

## Data Retention Policy

Raw data files should be retained for at least 1 year for audit and reproducibility purposes.

## Note

The actual raw data files have been moved to the parent directory for easier access in the analysis process. This directory remains as a placeholder in the project structure for future raw data extractions.
