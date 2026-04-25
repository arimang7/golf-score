---
name: csv-analysis-skill
description: Advanced analysis and visualization of CSV data using Pandas.
---

# CSV Analysis Skill

This skill enables deep analysis of CSV files, such as trade logs or market data exports.

## Capabilities

1.  **Data Cleaning**: Handle missing values and format dates.
2.  **Trend Analysis**: Identify trends, support/resistance, and patterns.
3.  **Visualization**: Suggest or generate code for Plotly/Matplotlib charts.
4.  **Summary Statistics**: Provide mean, median, volatility, and max drawdown.

## Usage Guide

The agent should:
1.  Read the CSV file using `pandas`.
2.  Verify the column names and data types.
3.  Perform the requested analysis (e.g., "Calculate win rate from these trades").
4.  Generate a summary report.

## Example Prompts
- "Analyze this `trades.csv` and show my monthly PnL."
- "What is the maximum drawdown in this price history?"
- "Plot the closing price and a 50-day moving average from this CSV."
