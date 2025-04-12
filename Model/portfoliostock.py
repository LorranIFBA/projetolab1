class PortfolioStock:
    def __init__(self, portfolio_stock_id=None, portfolio_id=None, stock_id=None, quantity=None, purchase_price=None, purchase_date=None):
        self._portfolio_stock_id = portfolio_stock_id
        self._portfolio_id = portfolio_id
        self._stock_id = stock_id
        self._quantity = quantity
        self._purchase_price = purchase_price
        self._purchase_date = purchase_date

    # Getters
    @property
    def portfolio_stock_id(self):
        return self._portfolio_stock_id

    @property
    def portfolio_id(self):
        return self._portfolio_id

    @property
    def stock_id(self):
        return self._stock_id

    @property
    def quantity(self):
        return self._quantity

    @property
    def purchase_price(self):
        return self._purchase_price

    @property
    def purchase_date(self):
        return self._purchase_date

    # Setters
    @quantity.setter
    def quantity(self, value):
        self._quantity = value

    @purchase_price.setter
    def purchase_price(self, value):
        self._purchase_price = value

    @purchase_date.setter
    def purchase_date(self, value):
        self._purchase_date = value

    def __str__(self):
        return f"PortfolioStock(portfolio_stock_id={self._portfolio_stock_id}, portfolio_id={self._portfolio_id}, stock_id={self._stock_id}, quantity={self._quantity}, purchase_price={self._purchase_price}, purchase_date={self._purchase_date})"