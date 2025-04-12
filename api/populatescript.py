import pandas as pd
from Controller.stockcontroller import StockController  # Import the StockController class
from stockdatacacher import StockDataCacher


csv_file_path = "stocks.csv"


def populate_stocks_table():
    try:

        stock_controller = StockController()

        df = pd.read_csv(csv_file_path)
        print(df)

        for index, row in df.iterrows():
            ticker = row["Ticker"]
            name = row["Name"]
            sector = row["Sector"]
            industry = row["Industry"]

            stock_controller.add_stock(None, ticker, name, sector, industry)

        print("Stock data inserted successfully!")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":

    stockController = StockController()

    stocklist = stockController.get_all_stocks()

    tickerlist = []

    for stock in stocklist:
        tickerlist.append(stock.ticker_symbol)

    cacher = StockDataCacher()

    for ticker_symbol in tickerlist:
        try:
            print(f"Caching historical data for {ticker_symbol}...")
            cacher.cache_historical_data(ticker_symbol)
            print("Historical caching completed successfully!")
        except ValueError as e:
            print(f"Error during historical caching: {e}")
