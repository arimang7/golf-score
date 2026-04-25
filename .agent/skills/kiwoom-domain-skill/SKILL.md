---
name: kiwoom-domain-skill
description: Interface for domestic stock trading and data via Kiwoom OpenAPI.
---

# Kiwoom Domain Skill

This skill allows the agent to interact directly with the domestic (Korean) stock market via the user's Kiwoom implementation.

## Capabilities

1.  **Market Data**: Fetch Korean stock prices, order books, and daily/minute charts.
2.  **Investor Analysis**: Get foreign and institutional net buying status.
3.  **Watchlist Integration**: Manage the user's stock watchlist.
4.  **Domestic Stock Info**: Detailed basic info for KRX/KOSPI stocks.

## Usage Guide

The agent should:
1.  Import functions from `d:\workspace_cli\kiwoom_stock\api_client.py`.
2.  Use `get_domestic_stkinfo(["code"])` for bulk metadata.
3.  Use `get_domestic_daily_chart("code")` for historical technical analysis.
4.  Use `get_domestic_netbuy("code")` to track smart money flows.

## Core Functions 🛠️
- `get_domestic_stkbasic(stk_cd)`: Basic OHLC + Volume.
- `get_domestic_mrkcond(stk_cd)`: Real-time Orderbook (Hoga).
- `get_domestic_daily_chart(stk_cd)`: 100 days of candle data.
- `get_domestic_min_chart(stk_cd, tick_dv)`: Intraday minute candles.

## Example Prompts
- "Check the institutional net buy for Samsung Electronics (005930) over the last few days."
- "Show me the 5-minute chart for SK Hynix (000660)."
- "What is the current order book (bid/ask) for Naver (035420)?"
