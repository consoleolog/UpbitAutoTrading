

class EMA:
    SHORT = "EMA_SHORT"
    MIDDLE = "EMA_MIDDLE"
    LONG = "EMA_LONG"

    def __init__(
            self,
            short:int = 10,
            middle:int = 20,
            long:int = 40,
    ):
        self.short = short
        self.middle = middle
        self.long = long

    def __str__(self):
        return f"""EMA(
            short={self.short},
            middle={self.middle},
            long={self.long}
        )"""