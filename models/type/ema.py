

class EMA:
    SHORT = "EMA_SHORT"
    MIDDLE = "EMA_MIDDLE"
    LONG = "EMA_LONG"

    def __init__(
            self,
            short:int = 10,
            middle:int = 20,
            long:int = 60,
    ):
        self.short = short
        self.middle = middle
        self.long = long