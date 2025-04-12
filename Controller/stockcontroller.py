from Model.stock import Stock
from Model.stockDAO import StockDAO


class StockController:
    def __init__(self):
        pass

    # Create
    def add_stock(self, stock_id: int, ticker_symbol: str, company_name: str, sector: str, industry: str):
        with StockDAO() as stock_dao:
            stock = Stock(stock_id, ticker_symbol, company_name, sector, industry)
            stock_dao.create_stock(stock)

    # Read
    def get_stock(self, stock_id: int) -> 'Stock':
        with StockDAO() as stock_dao:
            return stock_dao.get_stock_by_id(stock_id)

    def get_all_stocks(self) -> list['Stock']:
        with StockDAO() as stock_dao:
            return stock_dao.get_all_stocks()

    def get_stock_by_ticker_symbol(self, ticker_symbol: str) -> 'Stock':
        with StockDAO() as stock_dao:
            return stock_dao.get_stock_by_ticker_symbol(ticker_symbol)

    # Update
    def update_stock(self, stock_id: int, ticker_symbol: str = None, company_name: str = None, sector: str = None, industry: str = None):
        with StockDAO() as stock_dao:
            stock = stock_dao.get_stock_by_id(stock_id)
            if not stock:
                raise ValueError("Stock not found.")

            if ticker_symbol:
                stock.ticker_symbol = ticker_symbol
            if company_name:
                stock.company_name = company_name
            if sector:
                stock.sector = sector
            if industry:
                stock.industry = industry

            stock_dao.update_stock(stock)

    # Delete
    def delete_stock(self, stock_id: int):
        with StockDAO() as stock_dao:
            stock_dao.delete_stock(stock_id)




