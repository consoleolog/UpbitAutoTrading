from pandas import DataFrame

from models.order_dto import RequestOrderDto
from models.ma_dto import EmaDto, MacdDto
from models.candles_dto import ResponseCandlesDto

class StrategyComponent:

    def __init__(
            self,
            ema_dto: EmaDto,
            macd_dto: MacdDto,
    ):
        self.ema_dto = ema_dto
        self.macd_dto = macd_dto

    def get_ema(self, df: DataFrame):
        df[self.ema_dto.SHORT.name] = (
            df[ResponseCandlesDto.Df.CLOSE]
            .ewm(span=self.ema_dto.SHORT.value).mean()
        )

        df[self.ema_dto.MIDDLE.name] = (
            df[ResponseCandlesDto.Df.CLOSE]
            .ewm(span=self.ema_dto.MIDDLE.value).mean()
        )

        df[self.ema_dto.LONG.name] = (
            df[ResponseCandlesDto.Df.CLOSE]
            .ewm(span=self.ema_dto.LONG.value).mean()
        )
        return df

    def get_macd(self, df: DataFrame):
        df[self.macd_dto.UPPER.name] = (
            df[self.ema_dto.SHORT.name] - df[self.ema_dto.MIDDLE.name]
        )
        df[self.macd_dto.MIDDLE.name] = (
            df[self.ema_dto.SHORT.name] - df[self.ema_dto.LONG.name]
        )
        df[self.macd_dto.LOWER.name] = (
            df[self.ema_dto.MIDDLE.name] - df[self.ema_dto.LONG.name]
        )
        df[self.macd_dto.UPPER.INCREASE] = df[self.macd_dto.UPPER.name] > df[self.macd_dto.UPPER.name].shift(1)
        df[self.macd_dto.MIDDLE.INCREASE] = df[self.macd_dto.MIDDLE.name] > df[self.macd_dto.MIDDLE.name].shift(1)
        df[self.macd_dto.LOWER.INCREASE] = df[self.macd_dto.LOWER.name] > df[self.macd_dto.LOWER.name].shift(1)

        return df

    def before_order(self, df: DataFrame):
        up = df[self.macd_dto.UPPER.INCREASE]
        mid = df[self.macd_dto.MIDDLE.INCREASE]
        low = df[self.macd_dto.LOWER.INCREASE]

        UP_INCREASE = all([
            up.iloc[-1] == True,
            up.iloc[-2] == True,
            up.iloc[-3] == True,
        ])
        MID_INCREASE = all([
            mid.iloc[-1] == True,
            mid.iloc[-2] == True,
            mid.iloc[-3] == True,
        ])
        LOW_INCREASE = all([
            low.iloc[-1] == True,
            low.iloc[-2] == True,
            low.iloc[-3] == True,
        ])

        UP_DECREASE = all([
            up.iloc[-1] == False,
            up.iloc[-2] == False,
            up.iloc[-3] == False,
        ])

        MID_DECREASE = all([
            mid.iloc[-1] == False,
            mid.iloc[-2] == False,
            mid.iloc[-3] == False,
        ])

        LOW_DECREASE = all([
            mid.iloc[-1] == False,
            mid.iloc[-2] == False,
            mid.iloc[-3] == False,
        ])

        if UP_INCREASE and MID_INCREASE and LOW_INCREASE:
            return RequestOrderDto().set_mode("BUY").build()
        elif UP_DECREASE and MID_DECREASE and LOW_DECREASE:
            return RequestOrderDto().set_mode("SELL").build()
        else:
            return RequestOrderDto().set_mode("NOTHING").build()
