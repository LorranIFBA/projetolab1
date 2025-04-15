import mysql.connector
from Model.portfoliostock import PortfolioStock
from Controller.stockdatacontroller import StockDataController
from Controller.portfoliocontroller import PortfolioController
from DatabaseManager.databasemanager import DatabaseManager

class PortfolioStockDAO:
    def __init__(self):
        dbm = DatabaseManager()
        self.__connection = dbm.connection
        self.__cursor = dbm.cursor

    # Create
    def create_portfolio_stock(self, portfolio_stock: PortfolioStock):
        query = "INSERT INTO Portfolio_Stocks (portfolio_id, stock_id, quantity, purchase_price, purchase_date) VALUES (%s, %s, %s, %s, %s)"
        values = (portfolio_stock.portfolio_id, portfolio_stock.stock_id, portfolio_stock.quantity, portfolio_stock.purchase_price, portfolio_stock.purchase_date)
        self.__cursor.execute(query, values)
        self.__connection.commit()

    # Read
    def get_portfolio_stock_by_id(self, portfolio_stock_id: int) -> PortfolioStock:
        query = "SELECT portfolio_stock_id, portfolio_id, stock_id, quantity, purchase_price, purchase_date FROM Portfolio_Stocks WHERE portfolio_stock_id = %s"
        self.__cursor.execute(query, (portfolio_stock_id,))
        result = self.__cursor.fetchone()
        if result:
            return PortfolioStock(result[0], result[1], result[2], result[3], result[4], result[5])
        return None

    def get_portfolio_stock_by_portfolio_id_and_stock_id(self, portfolio_id: int, stock_id: int) -> PortfolioStock:
        query = "SELECT portfolio_stock_id, portfolio_id, stock_id, quantity, purchase_price, purchase_date FROM Portfolio_Stocks WHERE portfolio_id = %s AND stock_id = %s"
        self.__cursor.execute(query, (portfolio_id, stock_id,))
        result = self.__cursor.fetchone()
        if result:
            return PortfolioStock(result[0], result[1], result[2], result[3], result[4], result[5])
        return None

    def get_all_portfolio_stocks(self) -> list[PortfolioStock]:
        query = "SELECT portfolio_stock_id, portfolio_id, stock_id, quantity, purchase_price, purchase_date FROM Portfolio_Stocks"
        self.__cursor.execute(query)
        results = self.__cursor.fetchall()
        portfolio_stocks = []
        for result in results:
            portfolio_stocks.append(PortfolioStock(result[0], result[1], result[2], result[3], result[4], result[5]))
        return portfolio_stocks

    def get_all_portfolio_stocks_from_portfolio_id(self, portfolio_id) -> list[PortfolioStock]:
        query = "SELECT portfolio_stock_id, portfolio_id, stock_id, quantity, purchase_price, purchase_date FROM Portfolio_Stocks WHERE portfolio_id = %s"
        self.__cursor.execute(query, (portfolio_id,))
        results = self.__cursor.fetchall()
        portfolio_stocks = []
        for result in results:
            portfolio_stocks.append(PortfolioStock(result[0], result[1], result[2], result[3], result[4], result[5]))
        return portfolio_stocks

    # Update
    def update_portfolio_stock(self, portfolio_stock: PortfolioStock):
        query = "UPDATE Portfolio_Stocks SET quantity = %s, purchase_price = %s, purchase_date = %s WHERE portfolio_stock_id = %s"
        values = (portfolio_stock.quantity, portfolio_stock.purchase_price, portfolio_stock.purchase_date, portfolio_stock.portfolio_stock_id)
        self.__cursor.execute(query, values)
        self.__connection.commit()

    # Delete
    def delete_portfolio_stock(self, portfolio_stock_id: int):
        query = "DELETE FROM Portfolio_Stocks WHERE portfolio_stock_id = %s"
        self.__cursor.execute(query, (portfolio_stock_id,))
        self.__connection.commit()

    # Close database connection
    def close(self):
        if self.__cursor:
            self.__cursor.close()
        if self.__connection:
            self.__connection.close()

    # Context management (with block support)
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()