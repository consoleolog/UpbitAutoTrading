# -*- coding: utf-8 -*-
import numpy as np
from pandas import DataFrame

from constant import Stage, EMA


class EMADto:
    def __init__(self, data, period:int):
        self.val = data.ewm(span=period, adjust=False).mean()

    @staticmethod
    def get_stage(data: DataFrame) -> Stage:
        short, middle, long = data.iloc[-1][EMA.SHORT], data.iloc[-1][EMA.MID], data.iloc[-1][EMA.LONG]
        if short > middle > long:
            return Stage.STABLE_INCREASE
        elif middle > short > long:
            return Stage.END_OF_INCREASE
        elif middle > long > short:
            return Stage.START_OF_DECREASE
        elif long > middle > short:
            return Stage.STABLE_DECREASE
        elif long > short > middle:
            return Stage.END_OF_DECREASE
        elif short > long > middle:
            return Stage.START_OF_INCREASE

class MACDDto:
    def __init__(self, data:DataFrame ,period_short:int = 12, period_long:int = 26, period_signal: int = 9):
        ShortEMA = EMADto(data["close"], period_short).val
        LongEMA = EMADto(data["close"], period_long).val

        self.val = ShortEMA - LongEMA
        self.signal = EMADto(self.val, period_signal).val
        self.histogram = self.val - self.signal
        self.bullish = (self.val.shift(1) < self.signal.shift(1)) & (self.val > self.signal)
        self.bearish = (self.val.shift(1) > self.signal.shift(1)) & (self.val < self.signal)

class RSIDto:

    def __init__(self, data: DataFrame, period=14, period_sigal=9):
        delta = data["close"].diff()
        U = delta.clip(lower=0)
        D = -delta.clip(upper=0)
        AU = U.ewm(com=period - 1, min_periods=period).mean()
        AD = D.ewm(com=period - 1, min_periods=period).mean()

        rs = AU / AD
        rs.replace([np.inf, -np.inf], np.nan, inplace=True)
        rs.fillna(0, inplace=True)

        rsi = 100 - (100 / (1 + rs))
        self.val = rsi
        self.signal = EMADto(self.val, period_sigal).val
        self.histogram = self.val - self.signal
        self.bullish = ((self.val.shift(1) < self.signal.shift(1)) & (self.val > self.signal))
        self.bearish = ((self.val.shift(1) > self.signal.shift(1)) & (self.val < self.signal))

class StochasticDto:

    def __init__(self, data, k_len=10, k_smooth=6, d_smooth=6):
        low_price = data['low'].rolling(window=k_len, min_periods=1).min()
        high_price = data['high'].rolling(window=k_len, min_periods=1).max()
        k_fast = ((data["close"] - low_price) / (high_price - low_price)) * 100.0

        self.k_slow = k_fast.rolling(window=k_smooth, min_periods=1).mean()
        self.d_fast = k_fast.rolling(window=k_smooth, min_periods=1).mean()
        self.d_slow = self.d_fast.rolling(window=d_smooth, min_periods=1).mean()
        self.bullish = (self.d_fast.shift(1) < self.d_slow.shift(1)) & (self.d_fast > self.d_slow)
        self.bearish = (self.d_fast.shift(1) > self.d_slow.shift(1)) & (self.d_fast < self.d_slow)


class TickerInfo:
    def __init__(
            self,
            ask = None,
            ask_volume = None,
            average = None,
            base_volume = None,
            bid = None,
            bid_volume = None,
            change = None,
            close = None,
            datetime = None,
            high = None,
            info = None,
            last = None,
            low = None,
            open = None,
            percentage = None,
            previous_close = None,
            quote_volume = None,
            symbol = None,
            timestamp = None,
            vwap = None,
    ):
        self.ask = ask
        self.ask_volume = ask_volume
        self.average = average
        self.base_volume = base_volume
        self.bid = bid
        self.bid_volume = bid_volume
        self.change = change
        self.close = close
        self.datetime = datetime
        self.high = high
        self.info = info
        self.last = last
        self.low = low
        self.open = open
        self.percentage = percentage
        self.previous_close = previous_close
        self.quote_volume = quote_volume
        self.symbol = symbol
        self.timestamp = timestamp
        self.vwap = vwap

    @staticmethod
    def from_dict(dicts):
        return TickerInfo(
            ask = dicts['ask'],
            ask_volume = dicts['askVolume'],
            average = dicts['average'],
            base_volume = dicts['baseVolume'],
            bid = dicts['bid'],
            bid_volume = dicts['bidVolume'],
            change = dicts['change'],
            close = dicts['close'],
            datetime = dicts['datetime'],
            high = dicts['high'],
            info = dicts['info'],
            last = dicts['last'],
            low = dicts['low'],
            open = dicts['open'],
            percentage = dicts['percentage'],
            previous_close = dicts['previousClose'],
            quote_volume = dicts['quoteVolume'],
            symbol = dicts['symbol'],
            timestamp = dicts['timestamp'],
            vwap = dicts['vwap'],
        )


    def __str__(self):
        return f"""
        TickerInfo(
            ask = {self.ask},
            ask_volume = {self.ask_volume},
            average = {self.average},
            base_volume = {self.base_volume},
            bid = {self.bid},
            bid_volume = {self.bid_volume},
            change = {self.change},
            close = {self.close},
            datetime = {self.datetime},
            high = {self.high},
            info = {self.info},
            last = {self.last},
            low = {self.low},
            open = {self.open},
            percentage = {self.percentage},
            previous_close = {self.previous_close},
            quote_volume = {self.quote_volume},
            symbol = {self.symbol},
            timestamp = {self.timestamp},
            vwap = {self.vwap},
        )"""

class OrderInfo:
    def __init__(
        self,
        uuid = None,
        side = None,
        ord_type = None,
        price = None,
        state = None,
        market = None,
        created_at = None,
        reserved_fee = None,
        remaining_fee = None,
        paid_fee = None,
        locked = None,
        executed_volume = None,
        trades_count = None,
        volume = None,
        remaining_volume = None,
    ):
        self.uuid = uuid
        self.side = side
        self.ord_type = ord_type
        self.price = price
        self.state = state
        self.market = market
        self.created_at = created_at
        self.reserved_fee = reserved_fee
        self.remaining_fee = remaining_fee
        self.paid_fee = paid_fee
        self.locked = locked
        self.executed_volume = executed_volume
        self.trades_count = trades_count

    @staticmethod
    def from_buy(dicts):
        return OrderInfo(
            uuid = dicts['uuid'],
            side = dicts['side'],
            ord_type = dicts['ord_type'],
            price = dicts['price'],
            state = dicts['state'],
            market = dicts['market'],
            created_at = dicts['created_at'],
            reserved_fee = dicts['reserved_fee'],
            remaining_fee= dicts['remaining_fee'],
            paid_fee = dicts['paid_fee'],
            locked = dicts['locked'],
            executed_volume = dicts['executed_volume'],
            trades_count = dicts['trades_count']
        )

    @staticmethod
    def from_sell(dicts):
        return OrderInfo(
            uuid = dicts['uuid'],
            side = dicts['side'],
            ord_type = dicts['ord_type'],
            state = dicts['state'],
            market = dicts['market'],
            created_at = dicts['created_at'],
            volume= dicts['volume'],
            remaining_volume= dicts['remaining_volume'],
            reserved_fee = dicts['reserved_fee'],
            remaining_fee = dicts['remaining_fee'],
            paid_fee = dicts['paid_fee'],
            locked = dicts['locked'],
            executed_volume = dicts['executed_volume'],
            trades_count = dicts['trades_count']
        )