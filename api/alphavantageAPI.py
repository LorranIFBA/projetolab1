import requests

class AlphaVantageAPI:
    def __init__(self):
        self.api_key = "KW2MFCLQKWKAS6CZ"
        self.base_url = "https://www.alphavantage.co/query"

    def get_daily_stock_data(self, ticker_symbol: str):

        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker_symbol,
            "apikey": self.api_key,
            "outputsize": "full"
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if "Error Message" in data:
                raise ValueError(f"API Error: {data['Error Message']}")

            time_series = data.get("Time Series (Daily)", {})
            if not time_series:
                raise ValueError("No time series data found in API response.")

            return time_series
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to fetch data from Alpha Vantage API: {e}")


