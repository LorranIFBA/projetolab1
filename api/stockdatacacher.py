from datetime import datetime
from alphavantageAPI import AlphaVantageAPI
from Model.stockdataDAO import StockDataDAO
from Model.stockDAO import StockDAO
from Model.stockdata import StockData

class StockDataCacher:
    def __init__(self):
        self.alpha_vantage = AlphaVantageAPI()
        self.stock_dao = StockDAO()
        self.stock_data_dao = StockDataDAO()

    def cache_historical_data(self, ticker_symbol: str):

        stock = self.stock_dao.get_stock_by_ticker_symbol(ticker_symbol)
        if not stock:
            raise ValueError(f"Stock with ticker symbol '{ticker_symbol}' not found in the database.")

        stock_id = stock.stock_id

        print(f"Fetching historical stock data for {ticker_symbol}...")
        daily_data = self.alpha_vantage.get_daily_stock_data(ticker_symbol)

        print(f"Caching historical data for {ticker_symbol} (stock_id = {stock_id})...")
        for date, data in daily_data.items():
            existing_data = self.stock_data_dao.get_stock_data_by_stock_id_and_date(stock_id, date)
            if existing_data:
                print(f"Data for {date} already exists. Skipping...")
                continue

            stock_data = StockData(
                stock_data_id=None,
                stock_id=stock_id,
                date=date,
                open_price=float(data["1. open"]),
                close_price=float(data["4. close"]),
                high_price=float(data["2. high"]),
                low_price=float(data["3. low"]),
                volume=int(data["5. volume"])
            )

            # Insert new data
            self.stock_data_dao.create_stock_data(stock_data)
            print(f"Inserted data for {date}.")

        print(f"Historical caching completed for {ticker_symbol}.")

    def cache_incremental_data(self, ticker_symbol: str):
        stock = self.stock_dao.get_stock_by_ticker_symbol(ticker_symbol)
        if not stock:
            raise ValueError(f"Stock with ticker symbol '{ticker_symbol}' not found in the database.")

        stock_id = stock.stock_id

        latest_entry = self.stock_data_dao.get_latest_stock_data_by_stock_id(stock_id)
        latest_date_in_db = latest_entry.date if latest_entry else None

        print(f"Fetching incremental stock data for {ticker_symbol}...")
        daily_data = self.alpha_vantage.get_daily_stock_data(ticker_symbol)

        print(f"Caching incremental data for {ticker_symbol} (stock_id = {stock_id})...")
        for date, data in daily_data.items():
            api_date = datetime.strptime(date, "%Y-%m-%d").date()

            if latest_date_in_db and api_date <= latest_date_in_db:
                continue

            stock_data = StockData(
                stock_data_id=None,
                stock_id=stock_id,
                date=date,
                open_price=float(data["1. open"]),
                close_price=float(data["4. close"]),
                high_price=float(data["2. high"]),
                low_price=float(data["3. low"]),
                volume=int(data["5. volume"])
            )

            self.stock_data_dao.create_stock_data(stock_data)
            print(f"Inserted data for {date}.")

        print(f"Incremental caching completed for {ticker_symbol}.")

        print(f"Incremental caching completed for {ticker_symbol}.")