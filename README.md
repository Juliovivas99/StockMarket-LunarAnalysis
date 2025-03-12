# Stock Market & Lunar Phase Analysis

This project analyzes the relationship between lunar phases and stock market behavior for four major ETFs:

- SPY (S&P 500 ETF)
- QQQ (Nasdaq 100 ETF)
- DIA (Dow 30 ETF)
- IWM (Russell 2000 ETF)

## Project Structure

```
DataEngineeringProject2/
├── data/                    # Data files
│   ├── raw/                 # Raw data extracted from sources
│   └── processed/           # Processed data ready for analysis
├── reports/                 # Analysis reports
│   ├── data_engineering_report.pdf  # Comprehensive report
│   └── lunar_stock_analysis_report.md  # Markdown analysis report
├── scripts/                 # Python and PowerShell scripts
│   ├── extract_stock_data.py        # Extract stock price data
│   ├── extract_moon_data.py         # Extract lunar phase data
│   ├── upload_stock_blob.py         # Upload stock data to Azure Blob
│   ├── upload_moon_blob.py          # Upload lunar data to Azure Blob
│   ├── upload_stock_sql.py          # Transfer stock data to SQL DB
│   ├── upload_moon_sql.py           # Transfer lunar data to SQL DB
│   ├── azure_stock_lunar_analysis.py # Main analysis script
│   └── azure_automation_lunar_analysis.ps1  # Automation script
├── sql/                     # SQL queries
│   └── stock_lunar_analysis_queries.sql  # Analysis queries
├── visualizations/          # Charts and graphs
│   ├── correlation_heatmap.png       # Correlation analysis
│   └── returns_by_lunar_phase.png    # Returns by lunar phase
├── .env                     # Environment variables (credentials)
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## Project Components

### Data Pipeline Flow

1. **Data Extraction**: Extract stock price data from Yahoo Finance and lunar phase data from NASA API
2. **Data Storage**: Upload raw data to Azure Blob Storage containers
3. **Data Processing**: Transfer and transform data to Azure SQL Database
4. **Data Analysis**: Perform statistical analysis and correlation tests
5. **Visualization & Reporting**: Generate visualizations and comprehensive reports

### Database Details

- **Server**: stockdatapipeline-server.database.windows.net
- **Database**: StockPriceDB
- **Tables**:
  - SPY_StockPrices, QQQ_StockPrices, DIA_StockPrices, IWM_StockPrices
  - LunarPhases
  - StockLunarAnalysisResults (ANOVA test results)
  - LunarPhaseReturns (Average returns by lunar phase)

## Setup & Requirements

1. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

2. Configure environment variables in `.env` file:
   - Azure Storage Account credentials
   - Azure Blob Storage details
   - SQL Server connection string

## Analysis Performed

The analysis includes:

1. **Correlation Analysis**: Examines correlations between lunar phases and stock metrics (Close Price, Volume, Returns)
2. **Returns by Lunar Phase**: Calculates average daily returns for each lunar phase
3. **ANOVA Tests**: Checks if trading volume and returns vary significantly by lunar phase
4. **Visualization**: Generates heatmaps and bar charts to visualize the findings

## Automation

The analysis can be automated using:

- Azure Automation Account with the included PowerShell script
- Azure Data Factory pipelines
- SQL Server Agent jobs with scheduled queries

## Key Findings

The data analysis shows:

- Weak correlations between lunar phases and stock metrics (all below 0.03)
- Some variations in returns across lunar phases, but not statistically significant
- DIA (Dow 30 ETF) shows statistically significant volume variation by lunar phase (p < 0.05)
- Highest average returns during Full Moon (0.15%) and Last Quarter (0.15%) phases
- Lowest average returns during Waxing Crescent (-0.10%)
- Overall, lunar phases do not appear to have a meaningful impact on stock market behavior

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Created as part of an Azure Data Engineering project.
