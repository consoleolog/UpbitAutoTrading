
class EmaDto:
    def __init__(self, short=10, middle=20, long=40):
        self.short = short
        self.middle = middle
        self.long = long

        self.SHORT = self._EmaField(name="EMA_SHORT", value=self.short)
        self.MIDDLE = self._EmaField(name="EMA_MIDDLE", value=self.middle)
        self.LONG = self._EmaField(name="EMA_LONG", value=self.long)

    class _EmaField:
        def __init__(self, name, value):
            self.name = name
            self.value = value

        def __repr__(self):
            return f"{self.name}: {self.value}"

    def __repr__(self):
        return (f"EmaDto(short={self.short}, middle={self.middle}, long={self.long}, "
                f"SHORT={self.SHORT}, MIDDLE={self.MIDDLE}, LONG={self.LONG})")


class MacdDto:
    class UPPER:
        name = "MACD_UPPER"
        INCREASE = "MACD_UPPER_INCREASE"

    class MIDDLE:
        name = "MACD_MIDDLE"
        INCREASE = "MACD_MIDDLE_INCREASE"


    class LOWER:
        name = "MACD_LOWER"
        INCREASE = "MACD_LOWER_INCREASE"
