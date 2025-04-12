class StockData:
    def __init__(self, stock_data_id=None, stock_id=None, date=None, open_price=None, close_price=None, high_price=None, low_price=None, volume=None):
        self._stock_data_id = stock_data_id
        self._stock_id = stock_id
        self._date = date
        self._open_price = open_price
        self._close_price = close_price
        self._high_price = high_price
        self._low_price = low_price
        self._volume = volume

    # Getters
    @property
    def stock_data_id(self):
        return self._stock_data_id

    @property
    def stock_id(self):
        return self._stock_id

    @property
    def date(self):
        return self._date

    @property
    def open_price(self):
        return self._open_price

    @property
    def close_price(self):
        return self._close_price

    @property
    def high_price(self):
        return self._high_price

    @property
    def low_price(self):
        return self._low_price

    @property
    def volume(self):
        return self._volume

    # Setters
    @open_price.setter
    def open_price(self, value):
        self._open_price = value

    @close_price.setter
    def close_price(self, value):
        self._close_price = value

    @high_price.setter
    def high_price(self, value):
        self._high_price = value

    @low_price.setter
    def low_price(self, value):
        self._low_price = value

    @volume.setter
    def volume(self, value):
        self._volume = value

    def __str__(self):
        return f"StockData(stock_data_id={self._stock_data_id}, stock_id={self._stock_id}, date={self._date}, open_price={self._open_price}, close_price={self._close_price}, high_price={self._high_price}, low_price={self._low_price}, volume={self._volume})"