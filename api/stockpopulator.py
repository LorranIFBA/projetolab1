import requests
import time
from Model.stockDAO import StockDAO
from Model.stock import Stock

class StockPopulator:
    def __init__(self):
        self.api_key = "KW2MFCLQKWKAS6CZ"
        self.base_url = "https://www.alphavantage.co/query"
        self.stock_dao = StockDAO()

    def fetch_listed_stocks(self):
        params = {
            "function": "LISTING_STATUS",
            "apikey": self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()

            stocks = []
            for line in response.text.splitlines()[1:]:
                symbol, name, exchange, asset_type, ipo_date, delisting_date, status = line.split(",")
                if status == "Active" and asset_type == "Stock":
                    stocks.append({
                        "ticker_symbol": symbol,
                        "company_name": name,
                        "exchange": exchange,
                        "ipo_date": ipo_date,
                        "status": status
                    })

            return stocks
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to fetch data from Alpha Vantage API: {e}")

    def fetch_stock_overview(self, ticker_symbol: str):
        params = {
            "function": "OVERVIEW",
            "symbol": ticker_symbol,
            "apikey": self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if "Error Message" in data:
                raise ValueError(f"API Error for {ticker_symbol}: {data['Error Message']}")

            return data
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to fetch overview data for {ticker_symbol}: {e}")

    def populate_stocks_table(self):
        print("Fetching listed stocks from Alpha Vantage API...")
        stocks = self.fetch_listed_stocks()

        print(f"Found {len(stocks)} active stocks. Inserting into the Stocks table...")
        for stock_data in stocks:
            existing_stock = self.stock_dao.get_stock_by_ticker_symbol(stock_data["ticker_symbol"])
            if existing_stock:
                print(f"Stock with ticker symbol {stock_data['ticker_symbol']} already exists. Skipping...")
                continue

            try:
                print(f"Fetching overview data for {stock_data['ticker_symbol']}...")
                overview_data = self.fetch_stock_overview(stock_data["ticker_symbol"])

                sector = overview_data.get("Sector", "N/A")
                industry = overview_data.get("Industry", "N/A")

                stock = Stock(
                    stock_id=None,
                    ticker_symbol=stock_data["ticker_symbol"],
                    company_name=stock_data["company_name"],
                    sector=sector,
                    industry=industry
                )

                self.stock_dao.create_stock(stock)
                print(f"Inserted stock: {stock.ticker_symbol} - {stock.company_name} (Sector: {sector}, Industry: {industry})")

                time.sleep(12)

            except Exception as e:
                print(f"Error processing stock {stock_data['ticker_symbol']}: {e}")

        print("Stock population completed.")