import mysql.connector
from Model.portfolio import Portfolio


class PortfolioDAO:
    def __init__(self):
        # Open database connection
        self.__connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="lab12"
        )
        self.__cursor = self.__connection.cursor()

    # Create
    def create_portfolio(self, portfolio: Portfolio):
        query = "INSERT INTO Portfolios (user_id, portfolio_name) VALUES (%s, %s)"
        values = (portfolio.user_id, portfolio.portfolio_name)
        self.__cursor.execute(query, values)
        self.__connection.commit()

    # Read
    def get_portfolio_by_id(self, portfolio_id: int) -> Portfolio:
        query = "SELECT portfolio_id, user_id, portfolio_name, created_at FROM Portfolios WHERE portfolio_id = %s"
        self.__cursor.execute(query, (portfolio_id,))
        result = self.__cursor.fetchone()
        if result:
            return Portfolio(result[0], result[1], result[2], result[3])
        return None

    def get_all_portfolios(self) -> list[Portfolio]:
        query = "SELECT portfolio_id, user_id, portfolio_name, created_at FROM Portfolios"
        self.__cursor.execute(query)
        results = self.__cursor.fetchall()
        portfolios = []
        for result in results:
            portfolios.append(Portfolio(result[0], result[1], result[2], result[3]))
        return portfolios

    def get_portfolios_by_user_id(self, user_id: int) -> list[Portfolio]:
        query = "SELECT portfolio_id, user_id, portfolio_name, created_at FROM Portfolios WHERE user_id = %s"
        self.__cursor.execute(query, (user_id,))
        results = self.__cursor.fetchall()
        portfolios = []
        for result in results:
            portfolios.append(Portfolio(result[0], result[1], result[2], result[3]))
        return portfolios

    # Update
    def update_portfolio(self, portfolio: Portfolio):
        query = "UPDATE Portfolios SET portfolio_name = %s WHERE portfolio_id = %s"
        values = (portfolio.portfolio_name, portfolio.portfolio_id)
        self.__cursor.execute(query, values)
        self.__connection.commit()

    # Delete
    def delete_portfolio(self, portfolio_id: int):
        query = "DELETE FROM Portfolios WHERE portfolio_id = %s"
        self.__cursor.execute(query, (portfolio_id,))
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