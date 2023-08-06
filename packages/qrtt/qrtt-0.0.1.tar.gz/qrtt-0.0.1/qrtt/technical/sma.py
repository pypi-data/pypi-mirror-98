# import pandas as pd


def sma(ohlcv, period=10, ohlcv_series="close"):
    """
    Calculate simple moving average of the input data

    :param _ohlcv: ohlcv dataframe
    :type _ohlcv: pd.DataFrame
    :param period: how many periods to look back
    :type period: int
    :param ohlcv_series: which of the o/h/l/v to use
    :type ohlcv_series: str
    :return: pd.series
    """
    _ohlcv = ohlcv[[ohlcv_series]].copy(deep=True)
    indicator_values = _ohlcv[ohlcv_series].rolling(window=period, min_periods=period).mean()

    return indicator_values


def sma_dif(_ohlcv, short_period=12, long_period=26, percent_diff=True, ohlcv_series="close"):
    """
    If the value is above 0,
    it means short line is above the long line,
    momentum is strong
    """
    short = _ohlcv[ohlcv_series].rolling(window=short_period, min_periods=short_period).mean()
    long = _ohlcv[ohlcv_series].rolling(window=long_period, min_periods=long_period).mean()
    indicator_col = short / long - 1 if percent_diff else short - long

    return indicator_col
