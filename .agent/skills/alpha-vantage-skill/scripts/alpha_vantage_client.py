import os
import requests
import pandas as pd

class AlphaVantageClient:
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")

    def _get(self, params):
        if not self.api_key:
            return {"error": "API Key is missing. Please set ALPHA_VANTAGE_API_KEY."}
        
        params["apikey"] = self.api_key
        response = requests.get(self.BASE_URL, params=params)
        return response.json()

    def get_daily_price(self, symbol):
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": "compact"
        }
        return self._get(params)

    def get_rsi(self, symbol, interval="daily", time_period=14, series_type="close"):
        params = {
            "function": "RSI",
            "symbol": symbol,
            "interval": interval,
            "time_period": time_period,
            "series_type": series_type
        }
        return self._get(params)

if __name__ == "__main__":
    # Mock usage
    client = AlphaVantageClient(api_key="demo")
    print(client.get_daily_price("IBM"))
