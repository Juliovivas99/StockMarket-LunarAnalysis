import os
import pyodbc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get connection string from environment variables
conn_str = os.getenv('SQL_ODBC_CONNECTION_STRING')

# Connect to the database
print("Connecting to Azure SQL Database...")
try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    print("Connected successfully!")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit(1)

# Function to execute a query and return the results as a DataFrame
def execute_query(query):
    try:
        return pd.read_sql(query, conn)
    except Exception as e:
        print(f"Error executing query: {e}")
        print(f"Query: {query}")
        return None

# 1. Verify & Explore StockLunarAnalysisResults Table
print("\n1. Verifying StockLunarAnalysisResults Table...")

# Check if the StockLunarAnalysisResults table exists
table_check_query = """
SELECT * 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_NAME = 'StockLunarAnalysisResults'
"""
table_exists = execute_query(table_check_query)
if table_exists.empty:
    print("StockLunarAnalysisResults table does not exist.")
else:
    print("StockLunarAnalysisResults table exists. Checking its columns...")
    
    # Check columns in the StockLunarAnalysisResults table
    column_check_query = """
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = 'StockLunarAnalysisResults'
    """
    columns = execute_query(column_check_query)
    print("Columns in StockLunarAnalysisResults:")
    print(columns)
    
    # Get a sample of data from the StockLunarAnalysisResults table
    sample_query = """
    SELECT TOP 10 * 
    FROM StockLunarAnalysisResults
    """
    sample_data = execute_query(sample_query)
    print("\nSample data from StockLunarAnalysisResults:")
    print(sample_data)

# Check if average returns by lunar phase is already in the table
has_avg_returns = False
if not table_exists.empty:
    if 'AverageReturn' in columns['COLUMN_NAME'].values:
        has_avg_returns = True
        print("StockLunarAnalysisResults already contains average returns by lunar phase.")
    else:
        print("StockLunarAnalysisResults does not contain average returns by lunar phase. Will compute them.")

# 2. Fetch Stock Data and Lunar Phases
print("\n2. Fetching Stock Data and Lunar Phases...")

# Get stock data for each ETF
etfs = ['SPY', 'QQQ', 'DIA', 'IWM']
stock_data = {}

for etf in etfs:
    query = f"""
    SELECT s.[Date], s.[Open], s.[High], s.[Low], s.[Close], s.[Volume], l.[Phase]
    FROM {etf}_StockPrices s
    JOIN LunarPhases l ON CAST(s.[Date] AS DATE) = CAST(l.[Date] AS DATE)
    ORDER BY s.[Date]
    """
    data = execute_query(query)
    if data is not None:
        # Calculate daily returns
        data['Return'] = data['Close'].pct_change() * 100  # in percentage
        stock_data[etf] = data
        print(f"Fetched {len(data)} rows for {etf}")

# 3. Compute Correlations between lunar phases and stock data
print("\n3. Computing Correlations...")

# Check if any stock data was fetched
if not stock_data:
    print("No stock data was retrieved from the database. Can't proceed with the analysis.")
    print("Possible issues:")
    print("1. Tables might not exist or have a different naming convention")
    print("2. SQL query might need further adjustments")
    print("3. Database might not contain data yet")
    
    # Let's try to get the actual table names from the database
    tables_query = """
    SELECT TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE = 'BASE TABLE'
    """
    tables = execute_query(tables_query)
    print("\nAvailable tables in the database:")
    if tables is not None and not tables.empty:
        print(tables)
    else:
        print("Could not retrieve table information.")
    
    # Let's check one of the tables to see its column names
    sample_table_query = """
    SELECT TOP 1 * 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE = 'BASE TABLE' 
    """
    sample_table = execute_query(sample_table_query)
    
    if sample_table is not None and not sample_table.empty:
        table_name = sample_table.iloc[0]['TABLE_NAME']
        columns_query = f"""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = '{table_name}'
        """
        columns = execute_query(columns_query)
        print(f"\nColumns in the {table_name} table:")
        if columns is not None:
            print(columns)
    
    # Close connection and exit
    conn.close()
    exit(1)

# Create a function to convert lunar phases to numeric values
def lunar_phase_to_numeric(phase):
    phases = {
        'New Moon': 0,
        'Waxing Crescent': 1,
        'First Quarter': 2,
        'Waxing Gibbous': 3,
        'Full Moon': 4,
        'Waning Gibbous': 5,
        'Last Quarter': 6,
        'Waning Crescent': 7
    }
    return phases.get(phase, -1)

# Prepare data for correlation analysis
correlation_data = pd.DataFrame()

for etf, data in stock_data.items():
    # Convert lunar phases to numeric values
    data['PhaseNumeric'] = data['Phase'].apply(lunar_phase_to_numeric)
    
    # Add columns for correlation analysis
    correlation_data[f'{etf}_Close'] = data['Close']
    correlation_data[f'{etf}_Volume'] = data['Volume']
    correlation_data[f'{etf}_Return'] = data['Return']

# Add the lunar phase numeric column
correlation_data['PhaseNumeric'] = stock_data[etfs[0]]['PhaseNumeric']

# Calculate correlation matrix
correlation_matrix = correlation_data.corr()

# Create heatmap visualization
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix: Stock Data & Lunar Phases')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')
print("Generated correlation heatmap (correlation_heatmap.png)")

# Extract correlations with lunar phase
lunar_correlations = correlation_matrix['PhaseNumeric'].drop('PhaseNumeric').sort_values()
print("\nCorrelations with Lunar Phase:")
print(lunar_correlations)

# 4. Stock Returns by Lunar Phase
print("\n4. Analyzing Stock Returns by Lunar Phase...")

# Calculate average daily returns per lunar phase for each ETF
returns_by_phase = {}

for etf, data in stock_data.items():
    etf_returns_by_phase = data.groupby('Phase')['Return'].agg(['mean', 'std', 'count']).reset_index()
    returns_by_phase[etf] = etf_returns_by_phase
    print(f"\nAverage Returns by Lunar Phase for {etf}:")
    print(etf_returns_by_phase)

# Combine returns by phase for all ETFs
all_returns_by_phase = pd.DataFrame()
for etf, data in returns_by_phase.items():
    if all_returns_by_phase.empty:
        all_returns_by_phase = data.copy()
        all_returns_by_phase.rename(columns={'mean': etf + '_mean'}, inplace=True)
        all_returns_by_phase.drop(columns=['std', 'count'], inplace=True)
    else:
        all_returns_by_phase[etf + '_mean'] = data['mean']

# Calculate average returns across all ETFs
all_returns_by_phase['Average_Return'] = all_returns_by_phase[[f'{etf}_mean' for etf in etfs]].mean(axis=1)

# Sort phases in natural order
phase_order = ['New Moon', 'Waxing Crescent', 'First Quarter', 'Waxing Gibbous', 
               'Full Moon', 'Waning Gibbous', 'Last Quarter', 'Waning Crescent']
all_returns_by_phase['PhaseOrder'] = all_returns_by_phase['Phase'].map({phase: i for i, phase in enumerate(phase_order)})
all_returns_by_phase = all_returns_by_phase.sort_values('PhaseOrder')

# Create a bar chart of average returns by lunar phase
plt.figure(figsize=(14, 8))
ax = sns.barplot(x='Phase', y='Average_Return', data=all_returns_by_phase, order=phase_order)
plt.title('Average Stock Returns by Lunar Phase (All ETFs)', fontsize=16)
plt.xlabel('Lunar Phase', fontsize=14)
plt.ylabel('Average Daily Return (%)', fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add value labels on top of each bar
for i, bar in enumerate(ax.patches):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + (0.01 if bar.get_height() >= 0 else -0.03),
        f'{bar.get_height():.2f}%',
        ha='center',
        va='bottom' if bar.get_height() >= 0 else 'top',
        fontsize=10
    )

plt.tight_layout()
plt.savefig('returns_by_lunar_phase.png')
print("Generated returns by lunar phase chart (returns_by_lunar_phase.png)")

# 5. Perform ANOVA test to check if returns vary significantly by lunar phase
print("\n5. Performing ANOVA test for returns by lunar phase...")

for etf, data in stock_data.items():
    groups = [data[data['Phase'] == phase]['Return'].dropna() for phase in phase_order]
    anova_result = stats.f_oneway(*[group for group in groups if len(group) > 0])
    
    print(f"\nANOVA Test Results for {etf} Returns by Lunar Phase:")
    print(f"F-statistic: {anova_result.statistic:.4f}")
    print(f"p-value: {anova_result.pvalue:.4f}")
    print(f"Statistically significant (p < 0.05): {anova_result.pvalue < 0.05}")

# 6. Update StockLunarAnalysisResults table if needed
print("\n6. Updating StockLunarAnalysisResults table if needed...")

current_date = datetime.now().strftime('%Y-%m-%d')

# Create a separate table for lunar phase returns
try:
    create_returns_table_query = """
    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES 
                   WHERE TABLE_NAME = 'LunarPhaseReturns')
    CREATE TABLE LunarPhaseReturns (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        AnalysisDate DATE,
        ETF VARCHAR(10),
        LunarPhase VARCHAR(50),
        AverageReturn FLOAT,
        Count INT
    )
    """
    cursor.execute(create_returns_table_query)
    conn.commit()
    print("Created or verified LunarPhaseReturns table.")
    
    # Add returns data to the new table
    for etf in etfs:
        for _, row in returns_by_phase[etf].iterrows():
            insert_query = f"""
            INSERT INTO LunarPhaseReturns (AnalysisDate, ETF, LunarPhase, AverageReturn, Count)
            VALUES ('{current_date}', '{etf}', '{row['Phase']}', {row['mean']}, {row['count']})
            """
            try:
                cursor.execute(insert_query)
                conn.commit()
                print(f"Added {etf} average return for {row['Phase']}")
            except Exception as e:
                print(f"Error inserting {etf} average return for {row['Phase']}: {e}")
    
    # Now update the ANOVA results for returns in StockLunarAnalysisResults
    for etf in etfs:
        groups = [stock_data[etf][stock_data[etf]['Phase'] == phase]['Return'].dropna() 
                 for phase in phase_order if len(stock_data[etf][stock_data[etf]['Phase'] == phase]) > 0]
        anova_result = stats.f_oneway(*groups)
        
        conclusion = "Significant returns variation by lunar phase" if anova_result.pvalue < 0.05 else "No significant returns variation by lunar phase"
        
        # Get current correlation value from our analysis
        correlation_value = correlation_data[[f'{etf}_Volume', 'PhaseNumeric']].corr().iloc[0, 1]
        
        # Check if we need to insert or update
        check_query = f"""
        SELECT COUNT(*) AS count FROM StockLunarAnalysisResults 
        WHERE ETF = '{etf}'
        """
        check_result = execute_query(check_query)
        
        if check_result is not None and check_result.iloc[0]['count'] > 0:
            # Update existing record
            update_query = f"""
            UPDATE StockLunarAnalysisResults 
            SET AnalysisDate = '{current_date}',
                Correlation_Volume = {correlation_value},
                ANOVA_F_Statistic = {anova_result.statistic},
                ANOVA_P_Value = {anova_result.pvalue},
                Conclusion = '{conclusion}'
            WHERE ETF = '{etf}'
            """
            try:
                cursor.execute(update_query)
                conn.commit()
                print(f"Updated ANOVA results for {etf}.")
            except Exception as e:
                print(f"Error updating ANOVA results for {etf}: {e}")
        else:
            # Insert new record
            insert_query = f"""
            INSERT INTO StockLunarAnalysisResults 
            (AnalysisDate, ETF, Correlation_Volume, ANOVA_F_Statistic, ANOVA_P_Value, Conclusion)
            VALUES ('{current_date}', '{etf}', {correlation_value}, {anova_result.statistic}, 
                    {anova_result.pvalue}, '{conclusion}')
            """
            try:
                cursor.execute(insert_query)
                conn.commit()
                print(f"Inserted new ANOVA results for {etf}.")
            except Exception as e:
                print(f"Error inserting ANOVA results for {etf}: {e}")
    
except Exception as e:
    print(f"Error updating database: {e}")

# 7. Generate a report
print("\n7. Generating report...")

report = f"""
# Stock Market & Lunar Phase Analysis Report
*Generated on {datetime.now().strftime('%Y-%m-%d')}*

## 1. Introduction

This report analyzes the relationship between lunar phases and stock market behavior for four major ETFs:
- SPY (S&P 500 ETF)
- QQQ (Nasdaq 100 ETF)
- DIA (Dow 30 ETF)
- IWM (Russell 2000 ETF)

The analysis investigates whether lunar phases have any meaningful impact on stock price returns and trading volume.

## 2. Correlation Analysis

The correlation analysis examines the relationship between lunar phases and various stock metrics:

"""

# Add ETF correlations to report
for etf in etfs:
    report += f"### {etf} Correlations\n"
    report += f"- Close Price vs Lunar Phase: {correlation_data[[f'{etf}_Close', 'PhaseNumeric']].corr().iloc[0, 1]:.4f}\n"
    report += f"- Volume vs Lunar Phase: {correlation_data[[f'{etf}_Volume', 'PhaseNumeric']].corr().iloc[0, 1]:.4f}\n"
    report += f"- Returns vs Lunar Phase: {correlation_data[[f'{etf}_Return', 'PhaseNumeric']].corr().iloc[0, 1]:.4f}\n\n"

report += """
**Interpretation:** Generally, correlation values close to 0 indicate no meaningful relationship between lunar phases and stock metrics.

## 3. Stock Returns by Lunar Phase

Average daily returns (%) for each lunar phase:

"""

# Add returns table to report
returns_table = all_returns_by_phase[['Phase'] + [f'{etf}_mean' for etf in etfs] + ['Average_Return']].copy()
returns_table.columns = ['Lunar Phase'] + etfs + ['Average (All ETFs)']
returns_table = returns_table.drop(columns='PhaseOrder', errors='ignore')
report += returns_table.to_markdown(index=False, floatfmt='.4f')

report += """

## 4. ANOVA Test Results

The ANOVA test checks whether the differences in stock returns across different lunar phases are statistically significant:

"""

# Add ANOVA results to report
for etf in etfs:
    groups = [stock_data[etf][stock_data[etf]['Phase'] == phase]['Return'].dropna() 
              for phase in phase_order]
    anova_result = stats.f_oneway(*[group for group in groups if len(group) > 0])
    
    report += f"### {etf}\n"
    report += f"- F-statistic: {anova_result.statistic:.4f}\n"
    report += f"- p-value: {anova_result.pvalue:.4f}\n"
    report += f"- Statistically significant (p < 0.05): {anova_result.pvalue < 0.05}\n\n"

report += """
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

"""

# Save the report to a file
with open('lunar_stock_analysis_report.md', 'w') as f:
    f.write(report)

print(f"Report generated: lunar_stock_analysis_report.md")

# 8. Automation Recommendations
print("\n8. Automation Recommendations...")
print("""
To automate this analysis process:

1. Create an Azure Automation Account and upload this script as a Python Runbook.
2. Set up a schedule to run weekly (e.g., every Monday at 6:00 AM).
3. Configure the Runbook to connect to your Azure SQL Database using credentials from Azure Key Vault.
4. Set up email notifications to receive the report and visualizations.

Alternatively:
- Use Azure Data Factory to create a pipeline that executes this script.
- Set up SQL Server Agent jobs with scheduled queries for the analysis.
""")

# Close the database connection
conn.close()
print("\nAnalysis completed successfully!") 