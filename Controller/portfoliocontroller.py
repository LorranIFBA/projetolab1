from Model.portfolio import Portfolio
from Model.portfolioDAO import PortfolioDAO


class PortfolioController:
    def __init__(self):
        pass

    # Create
    def add_portfolio(self, portfolio_name: str, user_id: int):
        with PortfolioDAO() as portfolio_dao:
            portfolio = Portfolio(user_id=user_id, portfolio_name=portfolio_name)
            portfolio_dao.create_portfolio(portfolio)

    # Read
    def get_portfolio(self, portfolio_id: int) -> 'Portfolio':
        with PortfolioDAO() as portfolio_dao:
            return portfolio_dao.get_portfolio_by_id(portfolio_id)

    def get_all_portfolios(self) -> list['Portfolio']:
        with PortfolioDAO() as portfolio_dao:
            return portfolio_dao.get_all_portfolios()

    def get_portfolios_by_user_id(self, user_id: int) -> list[Portfolio]:
        with PortfolioDAO() as portfolio_dao:
            return portfolio_dao.get_portfolios_by_user_id(user_id)

    # Update
    def update_portfolio(self, portfolio_id: int, portfolio_name: str = None, user_id: int = None):
        with PortfolioDAO() as portfolio_dao:
            portfolio = portfolio_dao.get_portfolio_by_id(portfolio_id)
            if not portfolio:
                raise ValueError("Portfolio not found.")

            if portfolio_name:
                portfolio.portfolio_name = portfolio_name
            if user_id:
                portfolio.user_id = user_id

            portfolio_dao.update_portfolio(portfolio)

    # Delete
    def delete_portfolio(self, portfolio_id: int):
        with PortfolioDAO() as portfolio_dao:
            portfolio_dao.delete_portfolio(portfolio_id)



"""
from Controller.usercontroller import UserController


# Create a UserController instance
user_controller = UserController()

# Create a PortfolioController instance
portfolio_controller = PortfolioController()

# Test CREATE operation for User
print("Testing CREATE operation for User...")
try:
    user_controller.add_user(1, "john_doe", "john@example.com", "hashed_password")
    print("User created successfully!")
except Exception as e:
    print(f"Error creating user: {e}")

# Test CREATE operation for Portfolio
print("\nTesting CREATE operation for Portfolio...")
try:
    portfolio_controller.add_portfolio(1, "Tech Stocks", 1)  # Use user_id = 101
    print("Portfolio created successfully!")
except Exception as e:
    print(f"Error creating portfolio: {e}")

# Test READ operation (get_portfolio_by_id)
print("\nTesting READ operation (get_portfolio_by_id)...")
try:
    portfolio = portfolio_controller.get_portfolio(1)
    if portfolio:
        print(f"Portfolio found: ID={portfolio.portfolio_id}, Name={portfolio.portfolio_name}, User ID={portfolio.user_id}")
    else:
        print("Portfolio not found.")
except Exception as e:
    print(f"Error retrieving portfolio: {e}")

# Test READ operation (get_all_portfolios)
print("\nTesting READ operation (get_all_portfolios)...")
try:
    all_portfolios = portfolio_controller.get_all_portfolios()
    if all_portfolios:
        print("All portfolios:")
        for p in all_portfolios:
            print(f"ID={p.portfolio_id}, Name={p.portfolio_name}, User ID={p.user_id}")
    else:
        print("No portfolios found.")
except Exception as e:
    print(f"Error retrieving all portfolios: {e}")

# Test UPDATE operation
print("\nTesting UPDATE operation...")
try:
    portfolio_controller.update_portfolio(1, portfolio_name="Tech Investments")
    print("Portfolio updated successfully!")
except Exception as e:
    print(f"Error updating portfolio: {e}")

# Verify the update
print("\nVerifying UPDATE operation...")
try:
    updated_portfolio = portfolio_controller.get_portfolio(1)
    if updated_portfolio:
        print(f"Updated portfolio: ID={updated_portfolio.portfolio_id}, Name={updated_portfolio.portfolio_name}, User ID={updated_portfolio.user_id}")
    else:
        print("Portfolio not found after update.")
except Exception as e:
    print(f"Error retrieving updated portfolio: {e}")

# Test DELETE operation
print("\nTesting DELETE operation...")
try:
    portfolio_controller.delete_portfolio(1)
    print("Portfolio deleted successfully!")
except Exception as e:
    print(f"Error deleting portfolio: {e}")

# Verify the deletion
print("\nVerifying DELETE operation...")
try:
    deleted_portfolio = portfolio_controller.get_portfolio(1)
    if deleted_portfolio:
        print("Portfolio still exists after deletion.")
    else:
        print("Portfolio successfully deleted.")
except Exception as e:
    print(f"Error verifying deletion: {e}")"""