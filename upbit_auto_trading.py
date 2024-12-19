import pandas as pd

from logger import Logger
from upbit_provider_v2 import UpbitProviderV2
from multiprocessing.dummy import Pool as ThreadPool

upbit_provider = UpbitProviderV2()

tickers = ["KRW-BTC", "KRW-ETH"]

my_krw = upbit_provider.get_currency('KRW')

price = float(my_krw) / len(tickers)

def get_slope(df, num):
    return (df.iloc[-1] - df.iloc[-(1 + num)]) / num


def get_result(df, mode):
    df_slope_2 = get_slope(df, 2)
    df_slope_3 = get_slope(df, 3)
    df_slope_4 = get_slope(df, 4)

    df_signal = df.ewm(span=9).mean()
    df_signal_slope_2 = get_slope(df_signal, 2)
    df_signal_slope_3 = get_slope(df_signal, 3)
    df_signal_slope_4 = get_slope(df_signal, 4)

    if mode == "buy":
        return all([
            df_slope_2 > df_signal_slope_2 > 0,
            df_slope_3 > df_signal_slope_3 > 0,
            df_slope_4 > df_signal_slope_4 > 0,
        ])
    else:
        return all([
            0 < df_slope_2 < df_signal_slope_2,
            0 < df_slope_3 < df_signal_slope_3,
            0 < df_slope_4 < df_signal_slope_4,
        ])

def main(ticker: str):

    data = upbit_provider.get_minute_candles(
        market=ticker,
        to=None,
        count=200,
        unit=5
    )

    closing_prices = [d['trade_price'] for d in data]

    EMA_SHORT = pd.Series(closing_prices).ewm(span=10).mean()
    EMA_MID = pd.Series(closing_prices).ewm(span=20).mean()
    EMA_LONG = pd.Series(closing_prices).ewm(span=60).mean()

    ## MACD UPPER ##
    MACD_UP = EMA_SHORT - EMA_MID
    MACD_UP_BUY_RESULT = get_result(MACD_UP, "buy")
    MACD_UP_SELL_RESULT = get_result(MACD_UP, "sell")

    ## MACD MID ##
    MACD_MID = EMA_SHORT - EMA_LONG
    MACD_MID_BUY_RESULT = get_result(MACD_MID, "buy")
    MACD_MID_SELL_RESULT = get_result(MACD_MID, "sell")

    ## MACD LOWER ##
    MACD_LOW = EMA_MID - EMA_LONG
    MACD_LOW_BUY_RESULT = get_result(MACD_LOW, "buy")
    MACD_LOW_SELL_RESULT = get_result(MACD_LOW, "sell")

    mine = upbit_provider.get_currency(ticker.replace('KRW-', ''))

    if MACD_UP_BUY_RESULT and MACD_MID_BUY_RESULT and MACD_LOW_BUY_RESULT:
        upbit_provider.create_order_v2(
            market=ticker,
            side="bid",
            ord_type="price",
            price=price,
            volume=None,
            identifier=None,
            time_in_force=None
        )


    if MACD_UP_SELL_RESULT and MACD_MID_SELL_RESULT and MACD_LOW_SELL_RESULT and mine != 0:
        volume = upbit_provider.get_currency(ticker.replace('KRW-', ''))

        upbit_provider.create_order_v2(
            market=ticker,
            side="ask",
            ord_type="market",
            price=None,
            volume=volume,
            identifier=None,
            time_in_force=None
        )


pool = ThreadPool(processes=len(tickers))
result = pool.map(main, tickers)
pool.close()
pool.join()

logger = Logger().get_logger(__name__)
logger.info(result)
















