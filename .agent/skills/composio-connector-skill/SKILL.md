---
name: composio-connector-skill
description: Sends automated trading alerts to Slack, Discord, or Gmail.
---

# Composio Connector Skill

This skill bridges the agent with external communication apps to send alerts and reports.

## Capabilities

1.  **Slack Integration**: Send messages to channels or users.
2.  **Discord Integration**: Post to webhooks or channels.
3.  **Email Alerts**: Send summaries via Gmail/SMTP.

## Usage Guide

The agent should:
1.  Format the alert message clearly.
2.  Use the `scripts/alert_manager.py` (or provide the necessary code) to send the request.
3.  Confirm the delivery status.

## Example Prompts
- "Send a Slack alert if the price of AAPL crosses $200."
- "Email me a summary of today's trading performance."
- "Post a breakout alert to the #trading-signals Discord channel."
