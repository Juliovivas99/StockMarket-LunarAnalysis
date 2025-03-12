# Scripts Directory

This directory contains all scripts used in the Stock Market & Lunar Phase Analysis project.

## Python Scripts

### Data Extraction

- `extract_stock_data.py`: Extracts stock price data for multiple ETFs from Yahoo Finance API
- `extract_moon_data.py`: Extracts lunar phase data from NASA API

### Data Storage

- `upload_stock_blob.py`: Uploads stock data to Azure Blob Storage
- `upload_moon_blob.py`: Uploads lunar phase data to Azure Blob Storage
- `upload_stock_sql.py`: Transfers stock data from Azure Blob Storage to Azure SQL Database
- `upload_moon_sql.py`: Transfers lunar phase data from Azure Blob Storage to Azure SQL Database

### Analysis

- `azure_stock_lunar_analysis.py`: Main analysis script that:
  - Connects to Azure SQL Database
  - Performs statistical analysis (correlations, ANOVA tests)
  - Generates visualizations
  - Creates reports
  - Updates database tables with results

## PowerShell Scripts

- `azure_automation_lunar_analysis.ps1`: PowerShell script for automating the analysis with Azure Automation

## Usage

### Data Pipeline Execution

The data pipeline should be executed in the following order:

1. Extract data

```bash
python extract_stock_data.py
python extract_moon_data.py
```

2. Upload data to Azure Blob Storage

```bash
python upload_stock_blob.py
python upload_moon_blob.py
```

3. Transfer data to Azure SQL Database

```bash
python upload_stock_sql.py
python upload_moon_sql.py
```

4. Run analysis

```bash
python azure_stock_lunar_analysis.py
```

### Automation

To set up automation with Azure Automation:

1. Create an Azure Automation Account
2. Upload `azure_stock_lunar_analysis.py` as a Python Runbook
3. Upload `azure_automation_lunar_analysis.ps1` as a PowerShell Runbook
4. Set up schedule to run weekly

## Dependencies

All scripts require the Python packages specified in `requirements.txt`, including:

- pyodbc
- pandas
- matplotlib
- seaborn
- scipy
- python-dotenv

## Environment Setup

The scripts use environment variables defined in `.env` file for:

- Azure Storage Account credentials
- Azure Blob Storage container details
- SQL Server connection string

## Error Handling

All scripts include error handling for:

- API connection failures
- Azure Blob Storage upload issues
- SQL database connection problems
- Data processing errors

## Notes

- Scripts are designed to be idempotent where possible
- Logging is provided to track execution progress
- Each script focuses on a single responsibility in the data pipeline
