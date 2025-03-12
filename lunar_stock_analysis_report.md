
# Stock Market & Lunar Phase Analysis Report
*Generated on 2025-03-12*

## 1. Introduction

This report analyzes the relationship between lunar phases and stock market behavior for four major ETFs:
- SPY (S&P 500 ETF)
- QQQ (Nasdaq 100 ETF)
- DIA (Dow 30 ETF)
- IWM (Russell 2000 ETF)

The analysis investigates whether lunar phases have any meaningful impact on stock price returns and trading volume.

## 2. Correlation Analysis

The correlation analysis examines the relationship between lunar phases and various stock metrics:

### SPY Correlations
- Close Price vs Lunar Phase: -0.0119
- Volume vs Lunar Phase: 0.0199
- Returns vs Lunar Phase: 0.0194

### QQQ Correlations
- Close Price vs Lunar Phase: -0.0118
- Volume vs Lunar Phase: 0.0259
- Returns vs Lunar Phase: 0.0256

### DIA Correlations
- Close Price vs Lunar Phase: -0.0114
- Volume vs Lunar Phase: 0.0197
- Returns vs Lunar Phase: 0.0076

### IWM Correlations
- Close Price vs Lunar Phase: -0.0027
- Volume vs Lunar Phase: 0.0206
- Returns vs Lunar Phase: 0.0158


**Interpretation:** Generally, correlation values close to 0 indicate no meaningful relationship between lunar phases and stock metrics.

## 3. Stock Returns by Lunar Phase

Average daily returns (%) for each lunar phase:

| Lunar Phase     |     SPY |     QQQ |     DIA |     IWM |   Average (All ETFs) |
|:----------------|--------:|--------:|--------:|--------:|---------------------:|
| New Moon        |  0.0827 |  0.0376 |  0.1319 |  0.1073 |               0.0899 |
| Waxing Crescent | -0.0824 | -0.0963 | -0.0963 | -0.1359 |              -0.1027 |
| First Quarter   |  0.1139 |  0.2174 |  0.0553 |  0.0131 |               0.0999 |
| Waxing Gibbous  |  0.0816 |  0.0924 |  0.0848 |  0.1145 |               0.0933 |
| Full Moon       |  0.1385 |  0.1447 |  0.1255 |  0.2026 |               0.1528 |
| Waning Gibbous  |  0.0036 |  0.0124 |  0.0136 |  0.0212 |               0.0127 |
| Last Quarter    |  0.1708 |  0.1707 |  0.1755 |  0.0902 |               0.1518 |
| Waning Crescent |  0.0635 |  0.1327 | -0.0050 |  0.0662 |               0.0644 |

## 4. ANOVA Test Results

The ANOVA test checks whether the differences in stock returns across different lunar phases are statistically significant:

### SPY
- F-statistic: 0.6485
- p-value: 0.7159
- Statistically significant (p < 0.05): False

### QQQ
- F-statistic: 0.6551
- p-value: 0.7103
- Statistically significant (p < 0.05): False

### DIA
- F-statistic: 0.8439
- p-value: 0.5509
- Statistically significant (p < 0.05): False

### IWM
- F-statistic: 0.5564
- p-value: 0.7916
- Statistically significant (p < 0.05): False


## 5. SQL Queries Used

The following SQL queries were used in this analysis:

```sql
-- Join stock prices with lunar phases
SELECT s.[Date], s.[Open], s.[High], s.[Low], s.[Close], s.[Volume], l.[Phase]
FROM ETF_StockPrices s
JOIN LunarPhases l ON CAST(s.[Date] AS DATE) = CAST(l.[Date] AS DATE)
ORDER BY s.[Date]
```

```sql
-- Check StockLunarAnalysisResults table structure
SELECT COLUMN_NAME 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'StockLunarAnalysisResults'
```

```sql
-- Create StockLunarAnalysisResults table (if needed)
CREATE TABLE StockLunarAnalysisResults (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    ETF VARCHAR(10),
    TestType VARCHAR(50),
    LunarPhase VARCHAR(50),
    Result FLOAT,
    PValue FLOAT,
    CreatedAt DATETIME DEFAULT GETDATE()
)
```

```sql
-- Insert ANOVA test results
INSERT INTO StockLunarAnalysisResults (ETF, TestType, LunarPhase, Result, PValue)
VALUES ('ETF', 'ANOVA Returns', 'All', F_statistic, p_value)
```

```sql
-- Insert average returns by lunar phase
INSERT INTO StockLunarAnalysisResults (ETF, TestType, LunarPhase, Result, PValue)
VALUES ('ETF', 'Average Return', 'Lunar Phase', average_return, NULL)
```

## 6. Conclusion

Based on the analysis of stock market data and lunar phases:

1. **Correlation Analysis:** The correlations between lunar phases and stock metrics (Close Price, Volume, Returns) are very weak, suggesting no meaningful relationship.

2. **Returns by Lunar Phase:** While there are some variations in average returns across different lunar phases, these differences are generally small and inconsistent across ETFs.

3. **Statistical Significance:** The ANOVA test results indicate that the differences in stock returns across lunar phases are not statistically significant (p > 0.05) for most ETFs.

4. **Overall Assessment:** The data does not support the hypothesis that lunar phases have a meaningful impact on stock market behavior. Any observed patterns are likely due to random chance rather than a causal relationship.

## 7. Automation Process

This analysis can be automated to run on a regular schedule using:
- Azure Automation Account with Python Runbooks
- Azure Data Factory pipelines
- SQL Server Agent jobs with scheduled queries

The recommended approach is to set up a weekly refresh to update the StockLunarAnalysisResults table with new data.

