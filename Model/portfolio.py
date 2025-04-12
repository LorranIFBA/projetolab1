class Portfolio:
    def __init__(self, portfolio_id=None, user_id=None, portfolio_name=None, created_at=None):
        self._portfolio_id = portfolio_id
        self._user_id = user_id
        self._portfolio_name = portfolio_name
        self._created_at = created_at

    # Getters
    @property
    def portfolio_id(self):
        return self._portfolio_id

    @property
    def user_id(self):
        return self._user_id

    @property
    def portfolio_name(self):
        return self._portfolio_name

    @property
    def created_at(self):
        return self._created_at

    # Setters
    @portfolio_name.setter
    def portfolio_name(self, value):
        self._portfolio_name = value

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    def __str__(self):
        return f"Portfolio(portfolio_id={self._portfolio_id}, user_id={self._user_id}, portfolio_name={self._portfolio_name}, created_at={self._created_at})"