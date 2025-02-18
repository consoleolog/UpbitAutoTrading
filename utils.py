# -*- coding: utf-8 -*-
import exchange
from constant import EMA, MACD, STOCHASTIC, RSI
from dto import EMADto, MACDDto, StochasticDto, RSIDto


def get_data(ticker, timeframe, short_period = 5, mid_period= 20, long_period = 40):
    data = exchange.get_candles(ticker, timeframe)

    # EMA
    data[EMA.SHORT] = EMADto(data["close"], short_period).val
    data[EMA.MID] = EMADto(data["close"], mid_period).val
    data[EMA.LONG] = EMADto(data["close"], long_period).val

    # MACD
    ShortMACD = MACDDto(data, 10, 20)
    data[MACD.SHORT] = ShortMACD.val
    data[MACD.SHORT_SIG]  = ShortMACD.signal
    data[MACD.SHORT_HIST] = ShortMACD.histogram
    data[MACD.SHORT_BULLISH] = ShortMACD.bullish
    data[MACD.SHORT_BEARISH] = ShortMACD.bearish

    LongMACD = MACDDto(data, 12, 26)
    data[MACD.LONG] = LongMACD.val
    data[MACD.LONG_SIG] = LongMACD.signal
    data[MACD.LONG_HIST] = LongMACD.histogram
    data[MACD.LONG_BULLISH] = LongMACD.bullish
    data[MACD.LONG_BEARISH] = LongMACD.bearish

    # Stochastic
    stochastic = StochasticDto(data, 12, 3, 3)
    data[STOCHASTIC.K_SLOW] = stochastic.d_fast
    data[STOCHASTIC.D_FAST] = stochastic.d_fast
    data[STOCHASTIC.D_SLOW] = stochastic.d_slow
    data[STOCHASTIC.BULLISH] = stochastic.bullish
    data[STOCHASTIC.BEARISH] = stochastic.bearish

    # RSI
    ShortRSI = RSIDto(data, 9)
    data[RSI.SHORT] = ShortRSI.val
    data[RSI.SHORT_SIG] = ShortRSI.signal
    data[RSI.SHORT_BULLISH] = ShortRSI.bullish
    data[RSI.SHORT_BEARISH] = ShortRSI.bearish

    LongRSI = RSIDto(data, 14)
    data[RSI.LONG] = LongRSI.val
    data[RSI.LONG_SIG] = LongRSI.signal
    data[RSI.LONG_BULLISH] = LongRSI.bullish
    data[RSI.LONG_BEARISH] = LongRSI.bearish

    return data

def get_profit(order, curr_price):
    buy_price = float(order["price"])
    return ((curr_price - buy_price) / buy_price) * 100.0