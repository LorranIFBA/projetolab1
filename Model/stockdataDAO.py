import mysql.connector
from Model.stockdata import StockData


class StockDataDAO:
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
    def create_stock_data(self, stock_data: StockData):
        query = "INSERT INTO Stock_Data (stock_id, date, open_price, close_price, high_price, low_price, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (
            stock_data.stock_id,
            stock_data.date,
            stock_data.open_price,
            stock_data.close_price,
            stock_data.high_price,
            stock_data.low_price,
            stock_data.volume
        )
        self.__cursor.execute(query, values)
        self.__connection.commit()

    # Read
    def get_stock_data_by_id(self, stock_data_id: int) -> StockData:
        query = "SELECT stock_data_id, stock_id, date, open_price, close_price, high_price, low_price, volume FROM Stock_Data WHERE stock_data_id = %s"
        self.__cursor.execute(query, (stock_data_id,))
        result = self.__cursor.fetchone()
        if result:
            return StockData(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
        return None

    def get_all_stock_data(self) -> list[StockData]:
        query = "SELECT stock_data_id, stock_id, date, open_price, close_price, high_price, low_price, volume FROM Stock_Data"
        self.__cursor.execute(query)
        results = self.__cursor.fetchall()
        stock_data_list = []
        for result in results:
            stock_data_list.append(StockData(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7]))
        return stock_data_list

    # Update
    def update_stock_data(self, stock_data: StockData):
        query = "UPDATE Stock_Data SET open_price = %s, close_price = %s, high_price = %s, low_price = %s, volume = %s WHERE stock_data_id = %s"
        values = (stock_data.open_price, stock_data.close_price, stock_data.high_price, stock_data.low_price, stock_data.volume, stock_data.stock_data_id)
        self.__cursor.execute(query, values)
        self.__connection.commit()

    # Delete
    def delete_stock_data(self, stock_data_id: int):
        query = "DELETE FROM Stock_Data WHERE stock_data_id = %s"
        self.__cursor.execute(query, (stock_data_id,))
        self.__connection.commit()

    def get_stock_data_by_stock_id_and_date(self, stock_id: int, date: str) -> 'StockData':
        query = "SELECT * FROM Stock_Data WHERE stock_id = %s AND date = %s"
        self.__cursor.execute(query, (stock_id, date))
        result = self.__cursor.fetchone()
        if result:
            return StockData(*result)
        return None

    def get_latest_stock_data_by_stock_id(self, stock_id: int) -> 'StockData':
        query = "SELECT * FROM Stock_Data WHERE stock_id = %s ORDER BY date DESC LIMIT 1"
        self.__cursor.execute(query, (stock_id,))
        result = self.__cursor.fetchone()
        if result:
            return StockData(*result)
        return None

    def get_all_stock_data_from_stock_id(self, stock_id: int) -> list[StockData]:
        query = "SELECT stock_data_id, stock_id, date, open_price, close_price, high_price, low_price, volume FROM Stock_Data WHERE stock_id = %s"
        self.__cursor.execute(query, (stock_id,))
        results = self.__cursor.fetchall()
        stock_data_list = []
        for result in results:
            stock_data_list.append(
                StockData(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7]))
        return stock_data_list



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