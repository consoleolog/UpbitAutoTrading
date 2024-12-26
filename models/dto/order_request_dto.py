


class OrderRequestDto:

    def __init__(self,
                 ticker:str = None,
                 price:float = None,
                 volume:float = None,):
        self.ticker = ticker
        self.price = price
        self.volume = volume

    def __str__(self):
        return f"""OrderRequestDto(
        ticker={self.ticker},
        price={self.price},
        volume={self.volume}
        )"""