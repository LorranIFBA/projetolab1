from Model.portfoliostock import PortfolioStock
from Model.portfoliostockDAO import PortfolioStockDAO
from Controller.stockdatacontroller import StockDataController


class PortfolioStockController:
    def __init__(self):
        pass

    # Create
    def add_portfolio_stock(self, portfolio_stock_id: int, portfolio_id: int, stock_id: int, quantity: int, purchase_date: str):
        with PortfolioStockDAO() as portfolio_stock_dao:
            sdc = StockDataController()
            purchase_price = sdc.get_latest_stock_data_by_stock_id(stock_id).close_price
            portfolio_stock = PortfolioStock(portfolio_stock_id, portfolio_id, stock_id, quantity, purchase_price, purchase_date)
            portfolio_stock_dao.create_portfolio_stock(portfolio_stock)

    # Read
    def get_portfolio_stock(self, portfolio_stock_id: int) -> 'PortfolioStock':
        with PortfolioStockDAO() as portfolio_stock_dao:
            return portfolio_stock_dao.get_portfolio_stock_by_id(portfolio_stock_id)

    def get_portfolio_stock_by_portfolio_id_and_stock_id(self, portfolio_id:int, stock_id: int) -> PortfolioStock:
        with PortfolioStockDAO() as portfolio_stock_dao:
            return portfolio_stock_dao.get_portfolio_stock_by_portfolio_id_and_stock_id(portfolio_id, stock_id)

    def get_all_portfolio_stocks(self) -> list['PortfolioStock']:
        with PortfolioStockDAO() as portfolio_stock_dao:
            return portfolio_stock_dao.get_all_portfolio_stocks()

    def get_all_portfolio_stocks_from_portfolio_id(self, portfolio_id) -> list['PortfolioStock']:
        with PortfolioStockDAO() as portfolio_stock_dao:
            return portfolio_stock_dao.get_all_portfolio_stocks_from_portfolio_id(portfolio_id)

    # Update
    def update_portfolio_stock(self, portfolio_stock_id: int, quantity: int = None, purchase_price: float = None, purchase_date: str = None):
        with PortfolioStockDAO() as portfolio_stock_dao:
            portfolio_stock = portfolio_stock_dao.get_portfolio_stock_by_id(portfolio_stock_id)
            if not portfolio_stock:
                raise ValueError("Portfolio stock not found.")

            if quantity:
                portfolio_stock.quantity = quantity
            if purchase_price:
                portfolio_stock.purchase_price = purchase_price
            if purchase_date:
                portfolio_stock.purchase_date = purchase_date

            portfolio_stock_dao.update_portfolio_stock(portfolio_stock)

    # Delete
    def delete_portfolio_stock(self, portfolio_stock_id: int):
        with PortfolioStockDAO() as portfolio_stock_dao:
            portfolio_stock_dao.delete_portfolio_stock(portfolio_stock_id)

"""
from Controller.usercontroller import UserController
from Controller.portfoliocontroller import PortfolioController
from Controller.stockcontroller import StockController

# Create a UserController instance
user_controller = UserController()

# Create a PortfolioController instance
portfolio_controller = PortfolioController()

# Create a StockController instance
stock_controller = StockController()

# Create a PortfolioStockController instance
portfolio_stock_controller = PortfolioStockController()

# Test CREATE operation for User
print("Testing CREATE operation for User...")
try:
    user_id = 1  # Define the user_id to use
    user_controller.add_user(user_id, "john_doe", "john@example.com", "hashed_password")
    print(f"User created successfully with user_id = {user_id}!")
except Exception as e:
    print(f"Error creating user: {e}")

# Test CREATE operation for Portfolio
print("\nTesting CREATE operation for Portfolio...")
try:
    portfolio_id = 1  # Define the portfolio_id to use
    portfolio_controller.add_portfolio(portfolio_id, "Tech Stocks", user_id)
    print(f"Portfolio created successfully with portfolio_id = {portfolio_id}!")
except Exception as e:
    print(f"Error creating portfolio: {e}")

# Test CREATE operation for Stock
print("\nTesting CREATE operation for Stock...")
try:
    stock_id = 1  # Define the stock_id to use
    stock_controller.add_stock(stock_id, "AAPL", "Apple Inc.", "Technology", "Consumer Electronics")
    print(f"Stock created successfully with stock_id = {stock_id}!")
except Exception as e:
    print(f"Error creating stock: {e}")

# Test CREATE operation for PortfolioStock
print("\nTesting CREATE operation for PortfolioStock...")
try:
    portfolio_stock_id = 1
    quantity = 10
    purchase_price = 150.50
    purchase_date = "2023-10-01"

    print(f"Creating portfolio stock with portfolio_id = {portfolio_id} and stock_id = {stock_id}")
    portfolio_stock_controller.add_portfolio_stock(portfolio_stock_id, portfolio_id, stock_id, quantity, purchase_price, purchase_date)
    print("Portfolio stock created successfully!")
except Exception as e:
    print(f"Error creating portfolio stock: {e}")

# Test READ operation (get_portfolio_stock_by_id)
print("\nTesting READ operation (get_portfolio_stock_by_id)...")
try:
    portfolio_stock = portfolio_stock_controller.get_portfolio_stock(portfolio_stock_id)
    if portfolio_stock:
        print(f"Portfolio stock found: ID={portfolio_stock.portfolio_stock_id}, Portfolio ID={portfolio_stock.portfolio_id}, Stock ID={portfolio_stock.stock_id}, Quantity={portfolio_stock.quantity}, Purchase Price={portfolio_stock.purchase_price}, Purchase Date={portfolio_stock.purchase_date}")
    else:
        print("Portfolio stock not found.")
except Exception as e:
    print(f"Error retrieving portfolio stock: {e}")

# Test READ operation (get_all_portfolio_stocks)
print("\nTesting READ operation (get_all_portfolio_stocks)...")
try:
    all_portfolio_stocks = portfolio_stock_controller.get_all_portfolio_stocks()
    if all_portfolio_stocks:
        print("All portfolio stocks:")
        for ps in all_portfolio_stocks:
            print(f"ID={ps.portfolio_stock_id}, Portfolio ID={ps.portfolio_id}, Stock ID={ps.stock_id}, Quantity={ps.quantity}, Purchase Price={ps.purchase_price}, Purchase Date={ps.purchase_date}")
    else:
        print("No portfolio stocks found.")
except Exception as e:
    print(f"Error retrieving all portfolio stocks: {e}")

# Test UPDATE operation
print("\nTesting UPDATE operation...")
try:
    new_quantity = 15
    new_purchase_price = 160.75
    portfolio_stock_controller.update_portfolio_stock(portfolio_stock_id, quantity=new_quantity, purchase_price=new_purchase_price)
    print("Portfolio stock updated successfully!")
except Exception as e:
    print(f"Error updating portfolio stock: {e}")

# Verify the update
print("\nVerifying UPDATE operation...")
try:
    updated_portfolio_stock = portfolio_stock_controller.get_portfolio_stock(portfolio_stock_id)
    if updated_portfolio_stock:
        print(f"Updated portfolio stock: ID={updated_portfolio_stock.portfolio_stock_id}, Portfolio ID={updated_portfolio_stock.portfolio_id}, Stock ID={updated_portfolio_stock.stock_id}, Quantity={updated_portfolio_stock.quantity}, Purchase Price={updated_portfolio_stock.purchase_price}, Purchase Date={updated_portfolio_stock.purchase_date}")
    else:
        print("Portfolio stock not found after update.")
except Exception as e:
    print(f"Error retrieving updated portfolio stock: {e}")

# Test DELETE operation (only for PortfolioStockController)
print("\nTesting DELETE operation for PortfolioStock...")
try:
    portfolio_stock_controller.delete_portfolio_stock(portfolio_stock_id)
    print("Portfolio stock deleted successfully!")
except Exception as e:
    print(f"Error deleting portfolio stock: {e}")

# Verify the deletion
print("\nVerifying DELETE operation for PortfolioStock...")
try:
    deleted_portfolio_stock = portfolio_stock_controller.get_portfolio_stock(portfolio_stock_id)
    if deleted_portfolio_stock:
        print("Portfolio stock still exists after deletion.")
    else:
        print("Portfolio stock successfully deleted.")
except Exception as e:
    print(f"Error verifying deletion: {e}")"""