class Stock:
    def __init__(self, stock_id=None, ticker_symbol=None, company_name=None, sector=None, industry=None):
        self._stock_id = stock_id
        self._ticker_symbol = ticker_symbol
        self._company_name = company_name
        self._sector = sector
        self._industry = industry

    # Getters
    @property
    def stock_id(self):
        return self._stock_id

    @property
    def ticker_symbol(self):
        return self._ticker_symbol

    @property
    def company_name(self):
        return self._company_name

    @property
    def sector(self):
        return self._sector

    @property
    def industry(self):
        return self._industry

    # Setters
    @ticker_symbol.setter
    def ticker_symbol(self, value):
        self._ticker_symbol = value

    @company_name.setter
    def company_name(self, value):
        self._company_name = value

    @sector.setter
    def sector(self, value):
        self._sector = value

    @industry.setter
    def industry(self, value):
        self._industry = value

    def __str__(self):
        return f"Stock(stock_id={self._stock_id}, ticker_symbol={self._ticker_symbol}, company_name={self._company_name}, sector={self._sector}, industry={self._industry})"