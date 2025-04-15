import mysql.connector
from Model.stock import Stock
from DatabaseManager.databasemanager import DatabaseManager


class StockDAO:
    def __init__(self):
        dbm = DatabaseManager()
        self.__connection = dbm.connection
        self.__cursor = dbm.cursor

    # Create
    def create_stock(self, stock: Stock):
        query = "INSERT INTO Stocks (ticker_symbol, company_name, sector, industry) VALUES (%s, %s, %s, %s)"
        values = (stock.ticker_symbol, stock.company_name, stock.sector, stock.industry)
        self.__cursor.execute(query, values)
        self.__connection.commit()

    # Read
    def get_stock_by_id(self, stock_id: int) -> Stock:
        query = "SELECT stock_id, ticker_symbol, company_name, sector, industry FROM Stocks WHERE stock_id = %s"
        self.__cursor.execute(query, (stock_id,))
        result = self.__cursor.fetchone()
        if result:
            return Stock(result[0], result[1], result[2], result[3], result[4])
        return None

    def get_all_stocks(self) -> list[Stock]:
        query = "SELECT stock_id, ticker_symbol, company_name, sector, industry FROM Stocks"
        self.__cursor.execute(query)
        results = self.__cursor.fetchall()
        stocks = []
        for result in results:
            stocks.append(Stock(result[0], result[1], result[2], result[3], result[4]))
        return stocks

    # Update
    def update_stock(self, stock: Stock):
        query = "UPDATE Stocks SET ticker_symbol = %s, company_name = %s, sector = %s, industry = %s WHERE stock_id = %s"
        values = (stock.ticker_symbol, stock.company_name, stock.sector, stock.industry, stock.stock_id)
        self.__cursor.execute(query, values)
        self.__connection.commit()

    # Delete
    def delete_stock(self, stock_id: int):
        query = "DELETE FROM Stocks WHERE stock_id = %s"
        self.__cursor.execute(query, (stock_id,))
        self.__connection.commit()

    def get_stock_by_ticker_symbol(self, ticker_symbol: str) -> 'Stock':
        query = "SELECT * FROM Stocks WHERE ticker_symbol = %s"
        self.__cursor.execute(query, (ticker_symbol,))
        result = self.__cursor.fetchone()
        if result:
            return Stock(*result)
        return None


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