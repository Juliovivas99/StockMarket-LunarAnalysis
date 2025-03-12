# Processed Data Directory

This directory is intended to store data that has been cleaned, transformed, or otherwise processed from the raw data sources.

## Expected Contents

- Cleaned and preprocessed stock price datasets
- Merged datasets combining stock prices with lunar phases
- Aggregated data summarizing stock metrics by lunar phase
- Features engineered for statistical analysis

## Data Processing Operations

The following operations are typically performed on the data:

1. **Data Cleaning**

   - Handling missing values
   - Removing duplicate entries
   - Standardizing date formats

2. **Feature Engineering**

   - Calculating daily returns
   - Computing volatility metrics
   - Creating lunar phase indicators

3. **Data Transformation**
   - Normalizing volume data
   - Log transformations for statistical analysis
   - Creating pivot tables for analysis by lunar phase

## Processing Scripts

The data processing is performed by:

- `scripts/azure_stock_lunar_analysis.py` - Main analysis script that processes raw data

## Output Format

Processed data files are typically stored in the following formats:

- CSV files for tabular data
- Parquet files for larger datasets
- JSON files for structured data with nested elements

## Note

The processed data files are primarily stored in the Azure SQL Database. This directory remains as a placeholder in the project structure for any intermediate processed data files that need to be stored locally.
