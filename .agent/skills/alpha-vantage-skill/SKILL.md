---
name: alpha-vantage-skill
description: Fetches global stock market data and technical indicators from Alpha Vantage.
---

# Alpha Vantage Skill

This skill allows the agent to interact with the Alpha Vantage API to retrieve financial data.

## Capabilities

1.  **Stock Quotes**: Get real-time price data for global stocks.
2.  **Historical Data**: Retrieve daily, weekly, or monthly price history.
3.  **Technical Indicators**: Fetch RSI, SMA, EMA, MACD, etc.
4.  **Forex & Crypto**: Get exchange rates and digital currency data.

## Usage Guide

To use this skill, the agent should:
1.  Check if `ALPHA_VANTAGE_API_KEY` is present in the environments.
2.  Use the `scripts/alpha_vantage_client.py` to make requests.
3.  Parse the JSON response and provide summaries or charts.

## Example Prompts
- "Get the daily price history for TSLA for the last month."
- "What is the current RSI(14) for NVDA?"
- "Get the exchange rate from USD to KRW."
