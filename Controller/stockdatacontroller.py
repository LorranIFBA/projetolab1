from Model.stockdata import StockData
from Model.stockdataDAO import StockDataDAO
import plotly.graph_objs as go
import pandas as pd

from Controller.stockcontroller import StockController

class StockDataController:
    def __init__(self):
        pass

    # Create
    def add_stock_data(self, stock_data_id: int, stock_id: int, date: str, open_price: float, close_price: float, high_price: float, low_price: float, volume: int):
        with StockDataDAO() as stock_data_dao:
            stock_data = StockData(stock_data_id, stock_id, date, open_price, close_price, high_price, low_price, volume)
            stock_data_dao.create_stock_data(stock_data)

    # Read
    def get_stock_data(self, stock_data_id: int) -> 'StockData':
        with StockDataDAO() as stock_data_dao:
            return stock_data_dao.get_stock_data_by_id(stock_data_id)

    def get_all_stock_data(self) -> list['StockData']:
        with StockDataDAO() as stock_data_dao:
            return stock_data_dao.get_all_stock_data()

    def get_stock_data_by_id_and_date(self, stock_id: int, date: str) -> 'StockData':
        with StockDataDAO() as stock_data_dao:
            return stock_data_dao.get_stock_data_by_stock_id_and_date(stock_id, date)

    def get_latest_stock_data_by_stock_id(self, stock_id: int) -> 'StockData':
        with StockDataDAO() as stock_data_dao:
            return stock_data_dao.get_latest_stock_data_by_stock_id(stock_id)

    def get_all_stock_data_from_stock_id(self, stock_id: int) -> list['StockData']:
        with StockDataDAO() as stock_data_dao:
            return stock_data_dao.get_all_stock_data_from_stock_id(stock_id)

    # Update
    def update_stock_data(self, stock_data_id: int, open_price: float = None, close_price: float = None, high_price: float = None, low_price: float = None, volume: int = None):
        with StockDataDAO() as stock_data_dao:
            stock_data = stock_data_dao.get_stock_data_by_id(stock_data_id)
            if not stock_data:
                raise ValueError("Stock data not found.")

            if open_price:
                stock_data.open_price = open_price
            if close_price:
                stock_data.close_price = close_price
            if high_price:
                stock_data.high_price = high_price
            if low_price:
                stock_data.low_price = low_price
            if volume:
                stock_data.volume = volume

            stock_data_dao.update_stock_data(stock_data)

    def create_plot_data(self, stock_id):
        sc = StockController()
        df = pd.DataFrame([{"date": str(stockdata.date), "price": float(stockdata.close_price)} for stockdata in
                          self.get_all_stock_data_from_stock_id(stock_id)]).sort_values(by="date",ignore_index=True)
        data = go.Scatter(
                    x=df["date"],
                    y=df["price"],
                    mode="lines",
                    name=f"{sc.get_stock_by_ticker_symbol(ticker_symbol).company_name} Historical Data")
        return data


    # Delete
    def delete_stock_data(self, stock_data_id: int):
        with StockDataDAO() as stock_data_dao:
            stock_data_dao.delete_stock_data(stock_data_id)



"""
from Controller.stockcontroller import StockController

# Create a StockController instance
stock_controller = StockController()

# Create a StockDataController instance
stock_data_controller = StockDataController()

# Test CREATE operation for Stock
print("Testing CREATE operation for Stock...")
try:
    stock_id = 1  # Define the stock_id to use
    stock_controller.add_stock(stock_id, "AAPL", "Apple Inc.", "Technology", "Consumer Electronics")
    print(f"Stock created successfully with stock_id = {stock_id}!")
except Exception as e:
    print(f"Error creating stock: {e}")

# Test CREATE operation for StockData
print("\nTesting CREATE operation for StockData...")
try:
    stock_data_id = 1
    date = "2023-10-01"
    open_price = 150.00
    close_price = 152.00
    high_price = 153.00
    low_price = 149.00
    volume = 1000000

    print(f"Creating stock data with stock_id = {stock_id}")
    stock_data_controller.add_stock_data(stock_data_id, stock_id, date, open_price, close_price, high_price, low_price, volume)
    print("Stock data created successfully!")
except Exception as e:
    print(f"Error creating stock data: {e}")

# Test READ operation (get_stock_data_by_id)
print("\nTesting READ operation (get_stock_data_by_id)...")
try:
    stock_data = stock_data_controller.get_stock_data(stock_data_id)
    if stock_data:
        print(f"Stock data found: ID={stock_data.stock_data_id}, Stock ID={stock_data.stock_id}, Date={stock_data.date}, Close Price={stock_data.close_price}")
    else:
        print("Stock data not found.")
except Exception as e:
    print(f"Error retrieving stock data: {e}")

# Test READ operation (get_all_stock_data)
print("\nTesting READ operation (get_all_stock_data)...")
try:
    all_stock_data = stock_data_controller.get_all_stock_data()
    if all_stock_data:
        print("All stock data:")
        for sd in all_stock_data:
            print(f"ID={sd.stock_data_id}, Stock ID={sd.stock_id}, Date={sd.date}, Close Price={sd.close_price}")
    else:
        print("No stock data found.")
except Exception as e:
    print(f"Error retrieving all stock data: {e}")

# Test UPDATE operation
print("\nTesting UPDATE operation...")
try:
    new_close_price = 155.00
    new_volume = 1200000
    stock_data_controller.update_stock_data(stock_data_id, close_price=new_close_price, volume=new_volume)
    print("Stock data updated successfully!")
except Exception as e:
    print(f"Error updating stock data: {e}")

# Verify the update
print("\nVerifying UPDATE operation...")
try:
    updated_stock_data = stock_data_controller.get_stock_data(stock_data_id)
    if updated_stock_data:
        print(f"Updated stock data: ID={updated_stock_data.stock_data_id}, Stock ID={updated_stock_data.stock_id}, Date={updated_stock_data.date}, Close Price={updated_stock_data.close_price}")
    else:
        print("Stock data not found after update.")
except Exception as e:
    print(f"Error retrieving updated stock data: {e}")

# Test DELETE operation
print("\nTesting DELETE operation...")
try:
    stock_data_controller.delete_stock_data(stock_data_id)
    print("Stock data deleted successfully!")
except Exception as e:
    print(f"Error deleting stock data: {e}")

# Verify the deletion
print("\nVerifying DELETE operation...")
try:
    deleted_stock_data = stock_data_controller.get_stock_data(stock_data_id)
    if deleted_stock_data:
        print("Stock data still exists after deletion.")
    else:
        print("Stock data successfully deleted.")
except Exception as e:
    print(f"Error verifying deletion: {e}")"""

