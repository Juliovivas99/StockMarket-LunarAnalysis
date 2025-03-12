# SQL Directory

This directory contains SQL queries used in the Stock Market & Lunar Phase Analysis project.

## Files

- `stock_lunar_analysis_queries.sql`: Contains all SQL queries used for analyzing the relationship between stock market behavior and lunar phases

## Database Information

- **Server**: stockdatapipeline-server.database.windows.net
- **Database**: StockPriceDB
- **Connection**: ODBC Driver 18 for SQL Server

## Table Schema

### Stock Price Tables

Each ETF has its own table with identical schema:

**SPY_StockPrices, QQQ_StockPrices, DIA_StockPrices, IWM_StockPrices**

- Date (datetime): Trading date
- Open (float): Opening price
- High (float): Highest price during the day
- Low (float): Lowest price during the day
- Close (float): Closing price
- Volume (bigint): Trading volume
- Adj_Close (float): Adjusted closing price

### Lunar Phase Table

**LunarPhases**

- Date (datetime): Calendar date
- Phase (varchar): Lunar phase name
- PhaseAngle (float): Lunar phase angle in degrees

### Analysis Results Tables

**StockLunarAnalysisResults**

- AnalysisDate (date): Date when analysis was performed
- ETF (varchar): ETF ticker symbol
- Correlation_Volume (float): Correlation coefficient between lunar phase and trading volume
- ANOVA_F_Statistic (float): F-statistic from ANOVA test
- ANOVA_P_Value (float): P-value from ANOVA test
- Conclusion (varchar): Interpretation of statistical results

**LunarPhaseReturns**

- ID (int): Primary key
- AnalysisDate (date): Date when analysis was performed
- ETF (varchar): ETF ticker symbol
- LunarPhase (varchar): Lunar phase name
- AverageReturn (float): Average daily return during this lunar phase
- Count (int): Number of data points in the average

## Frequently Used Queries

### Join Stock Prices with Lunar Phases

```sql
SELECT s.[Date], s.[Open], s.[High], s.[Low], s.[Close], s.[Volume], l.[Phase]
FROM SPY_StockPrices s
JOIN LunarPhases l ON CAST(s.[Date] AS DATE) = CAST(l.[Date] AS DATE)
ORDER BY s.[Date];
```

### Query Average Returns by Lunar Phase

```sql
SELECT lr.LunarPhase,
       AVG(CASE WHEN lr.ETF = 'SPY' THEN lr.AverageReturn END) AS SPY_Return,
       AVG(CASE WHEN lr.ETF = 'QQQ' THEN lr.AverageReturn END) AS QQQ_Return,
       AVG(CASE WHEN lr.ETF = 'DIA' THEN lr.AverageReturn END) AS DIA_Return,
       AVG(CASE WHEN lr.ETF = 'IWM' THEN lr.AverageReturn END) AS IWM_Return,
       AVG(lr.AverageReturn) AS Average_Return
FROM LunarPhaseReturns lr
GROUP BY lr.LunarPhase;
```

### Query ANOVA Results

```sql
SELECT ETF, ANOVA_F_Statistic, ANOVA_P_Value, Conclusion
FROM StockLunarAnalysisResults
ORDER BY ETF;
```

## Notes

- SQL queries are executed through Python scripts using pyodbc
- The database schema was designed for efficient joining of stock and lunar data
- Consider adding indexes on date columns for performance optimization
- Azure SQL Database size and performance tier may need adjustment for larger datasets
