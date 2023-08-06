# Bollinger Bands (BB)

"""
There are three bands when using Bollinger Bands

Middle Band – 20 Day Simple Moving Average
Upper Band – 20 Day Simple Moving Average + (Standard Deviation x 2)
Lower Band – 20 Day Simple Moving Average - (Standard Deviation x 2)
"""


def _bb_calc(ohlcv, period=20, number_of_std=2, ohlcv_series="close"):
    """RETURN Pandas DataFrame the contains all the necessary values/calculations of the Bollinger Band Indicator"""
    _ohlcv = ohlcv[[ohlcv_series]].copy(deep=True)
    _ohlcv["mid_band"] = _ohlcv[ohlcv_series].rolling(window=period, min_periods=period).mean()
    # ddof=0 means Degree of Freedom is 0. This calculates the population STD,
    # rather than the sample STD.
    _ohlcv["std"] = _ohlcv[ohlcv_series].rolling(window=period, min_periods=period).std(ddof=0)
    _ohlcv["lower_band"] = _ohlcv["mid_band"] - number_of_std * _ohlcv["std"]
    _ohlcv["upper_band"] = _ohlcv["mid_band"] + number_of_std * _ohlcv["std"]
    return _ohlcv


def boll(ohlcv, period=20, number_of_std=2, ohlcv_series="close"):
    """RETURN Three variables for the Bollinger Band indicator"""
    _ohlcv = _bb_calc(ohlcv, period, number_of_std, ohlcv_series)
    return _ohlcv[["lower_band", "mid_band", "upper_band"]]


def percent_b(ohlcv, period=20, number_of_std=2, ohlcv_series="close"):
    _ohlcv = _bb_calc(ohlcv, period, number_of_std, ohlcv_series)
    indicator_values = (_ohlcv[ohlcv_series] - _ohlcv['lower_band']) / (_ohlcv['upper_band'] - _ohlcv['lower_band'])
    return indicator_values

