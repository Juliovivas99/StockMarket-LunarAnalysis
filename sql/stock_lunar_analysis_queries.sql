-- SQL Queries for Stock and Lunar Phase Analysis

-- 1. Join stock prices with lunar phases
SELECT s.[Date], s.[Open], s.[High], s.[Low], s.[Close], s.[Volume], l.[Phase]
FROM SPY_StockPrices s
JOIN LunarPhases l ON CAST(s.[Date] AS DATE) = CAST(l.[Date] AS DATE)
ORDER BY s.[Date];

-- Similar queries for QQQ, DIA, and IWM
SELECT s.[Date], s.[Open], s.[High], s.[Low], s.[Close], s.[Volume], l.[Phase]
FROM QQQ_StockPrices s
JOIN LunarPhases l ON CAST(s.[Date] AS DATE) = CAST(l.[Date] AS DATE)
ORDER BY s.[Date];

SELECT s.[Date], s.[Open], s.[High], s.[Low], s.[Close], s.[Volume], l.[Phase]
FROM DIA_StockPrices s
JOIN LunarPhases l ON CAST(s.[Date] AS DATE) = CAST(l.[Date] AS DATE)
ORDER BY s.[Date];

SELECT s.[Date], s.[Open], s.[High], s.[Low], s.[Close], s.[Volume], l.[Phase]
FROM IWM_StockPrices s
JOIN LunarPhases l ON CAST(s.[Date] AS DATE) = CAST(l.[Date] AS DATE)
ORDER BY s.[Date];

-- 2. Check if StockLunarAnalysisResults table exists
SELECT * 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_NAME = 'StockLunarAnalysisResults';

-- 3. Check columns in the StockLunarAnalysisResults table
SELECT COLUMN_NAME 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'StockLunarAnalysisResults';

-- 4. Get a sample of data from the StockLunarAnalysisResults table
SELECT TOP 10 * 
FROM StockLunarAnalysisResults;

-- 5. Create LunarPhaseReturns table for storing average returns by lunar phase
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES 
               WHERE TABLE_NAME = 'LunarPhaseReturns')
CREATE TABLE LunarPhaseReturns (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    AnalysisDate DATE,
    ETF VARCHAR(10),
    LunarPhase VARCHAR(50),
    AverageReturn FLOAT,
    Count INT
);

-- 6. Insert average returns for each ETF and lunar phase into LunarPhaseReturns table
INSERT INTO LunarPhaseReturns (AnalysisDate, ETF, LunarPhase, AverageReturn, Count)
VALUES ('2025-03-12', 'SPY', 'New Moon', 0.082732, 158);

-- 7. Update StockLunarAnalysisResults table with ANOVA results
UPDATE StockLunarAnalysisResults 
SET AnalysisDate = '2025-03-12',
    Correlation_Volume = 0.0199,
    ANOVA_F_Statistic = 0.6485,
    ANOVA_P_Value = 0.7159,
    Conclusion = 'No significant returns variation by lunar phase'
WHERE ETF = 'SPY';

-- 8. Insert new ANOVA results into StockLunarAnalysisResults table
INSERT INTO StockLunarAnalysisResults 
(AnalysisDate, ETF, Correlation_Volume, ANOVA_F_Statistic, ANOVA_P_Value, Conclusion)
VALUES ('2025-03-12', 'SPY', 0.0199, 0.6485, 0.7159, 'No significant returns variation by lunar phase');

-- 9. Query for average returns by lunar phase for all ETFs
SELECT lr.LunarPhase, 
       AVG(CASE WHEN lr.ETF = 'SPY' THEN lr.AverageReturn END) AS SPY_Return,
       AVG(CASE WHEN lr.ETF = 'QQQ' THEN lr.AverageReturn END) AS QQQ_Return,
       AVG(CASE WHEN lr.ETF = 'DIA' THEN lr.AverageReturn END) AS DIA_Return,
       AVG(CASE WHEN lr.ETF = 'IWM' THEN lr.AverageReturn END) AS IWM_Return,
       AVG(lr.AverageReturn) AS Average_Return
FROM LunarPhaseReturns lr
GROUP BY lr.LunarPhase
ORDER BY 
    CASE lr.LunarPhase
        WHEN 'New Moon' THEN 1
        WHEN 'Waxing Crescent' THEN 2
        WHEN 'First Quarter' THEN 3
        WHEN 'Waxing Gibbous' THEN 4
        WHEN 'Full Moon' THEN 5
        WHEN 'Waning Gibbous' THEN 6
        WHEN 'Last Quarter' THEN 7
        WHEN 'Waning Crescent' THEN 8
    END;

-- 10. Query ANOVA test results for all ETFs
SELECT ETF, ANOVA_F_Statistic, ANOVA_P_Value, Conclusion
FROM StockLunarAnalysisResults
ORDER BY ETF;

-- 11. Calculate correlation between lunar phases and trading volume
-- This is a conceptual query, actual implementation was done in Python
SELECT ETF, Correlation_Volume
FROM StockLunarAnalysisResults
ORDER BY Correlation_Volume DESC; 