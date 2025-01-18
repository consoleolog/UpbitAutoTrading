import pandas as pd
from pandas import DataFrame
from scipy.stats import linregress

from models.type.ema import EMA
from models.type.stage_type import StageType


def get_stage_from_ema(data: DataFrame):
    try:
        ema_short = data.iloc[-1][EMA.SHORT]
        ema_middle = data.iloc[-1][EMA.MIDDLE]
        ema_long = data.iloc[-1][EMA.LONG]
        if ema_short > ema_middle > ema_long:
            return StageType.STABLE_INCREASE
        elif ema_middle > ema_short > ema_long:
            return StageType.END_OF_INCREASE
        elif ema_middle > ema_long > ema_short:
            return StageType.START_OF_DECREASE
        elif ema_long > ema_middle > ema_short:
            return StageType.STABLE_DECREASE
        elif ema_long > ema_short > ema_middle:
            return StageType.END_OF_DECREASE
        elif ema_short > ema_long > ema_middle:
            return StageType.START_OF_INCREASE
        else:
            return 0
    except IndexError as err:
        print(err)
        return 0

def is_downward_trend(data):
    if len(data) < 2:
        return False

    x = list(range(len(data)))
    slope, _, _, _, _ = linregress(x, data)

    return slope < 0

def is_upward_trend(data):
    if len(data) < 2:
        return False

    x = list(range(len(data)))
    slope, _, _, _, _ = linregress(x, data)

    return slope > 0.6

def is_empty(value):
    if isinstance(value, pd.DataFrame):
        return value.empty
    return value == 0 or value is None


def get_slope(data):
    if len(data) < 2:
        return None
    x = list(range(len(data)))
    slope, _, _, _, _ = linregress(x, data)
    return slope
