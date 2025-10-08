class stock_data:
    """
    Model to represent a stock update.
    """
    def __init__(self, price: float, symbol: str, time: int, volume: int):
        self.price = price
        self.symbol = symbol
        self.time = time
        self.volume = volume

    def __repr__(self):
        return f"StockUpdate(symbol={self.symbol}, price={self.price}, time={self.time}, volume={self.volume})"
