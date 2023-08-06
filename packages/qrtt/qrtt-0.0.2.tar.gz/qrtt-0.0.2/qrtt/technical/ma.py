import numpy as np


def wma(ohlcv, period=10, ohlcv_series="close"):
    
    """
    Return the weighted moving average (WMA) values
    """
    _ohlcv = ohlcv[[ohlcv_series]].copy(deep=True).sort_index(ascending=True)
    weights = np.arange(1, period + 1)
    indicator_values = _ohlcv[ohlcv_series].rolling(window=period, min_periods=period).\
        apply(lambda x: np.dot(x, weights)/weights.sum(), raw=True)

    return indicator_values


def dema(ohlcv, period=10, ohlcv_series="close"):
    """Return the double exponential moving average (DEMA) values

    Args:
        ohlcv ([type]): [description]
        period (int, optional): [description]. Defaults to 10.
        ohlcv_series (str, optional): [description]. Defaults to "close".

    Returns:
        [type]: [description]
    """
    _ohlcv = ohlcv[[ohlcv_series]].copy(deep=True)
    _ohlcv['ema'] = _ohlcv[ohlcv_series].ewm(span=period, min_periods=period).mean()
    _ohlcv['ema_ema'] = _ohlcv['ema'].ewm(span=period, min_periods=period).mean()
    indicator_values = 2 *_ohlcv['ema'] - _ohlcv['ema_ema']
    return indicator_values


def tema(ohlcv, period=10, ohlcv_series="close"):
    """
    Returns the triple exponential moving average (TEMA)
    """
    _ohlcv = ohlcv[[ohlcv_series]].copy(deep=True)
    _ohlcv['ema'] = _ohlcv[ohlcv_series].ewm(span=period, min_periods=period).mean()
    _ohlcv['ema_ema'] = _ohlcv['ema'].ewm(span=period, min_periods=period).mean()
    _ohlcv['ema_ema_ema'] = _ohlcv['ema_ema'].ewm(span=period, min_periods=period).mean()
    indicator_values = 3 *_ohlcv['ema'] - 3 * _ohlcv['ema_ema'] + _ohlcv['ema_ema_ema']
    return indicator_values



def trima(ohlcv, period=10, ohlcv_series="close"):
    """ Return the triangular moving average (TRIMA) values

    Args:
        ohlcv ([type]): [description]
        period (int, optional): [description]. Defaults to 10.
        ohlcv_series (str, optional): [description]. Defaults to "close".
    """
    pass


def kama():
    pass



def mama():
    pass