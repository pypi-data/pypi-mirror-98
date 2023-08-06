import numpy as np


def rsi(ohlcv, period=14, ohlcv_series="close"):
    """
    RSI CALCULATION

    The very first calculations for average gain and average loss are simple n-period averages:

        First Average Gain = Sum of Gains over the past n periods / n.
        First Average Loss = Sum of Losses over the past n periods / n

    The second, and subsequent, calculations are based on the prior averages and the current gain loss:

        Average Gain = [(previous Average Gain) x (n-1) + current Gain] / n.
        Average Loss = [(previous Average Loss) x (n-1) + current Loss] / n.

    RS = Average Gain / Average Loss
    RSI = 100 - (100 / (1 + RS))

    """
    _ohlcv = ohlcv[[ohlcv_series]].copy(deep=True)
    _ohlcv["diff"] = _ohlcv[ohlcv_series].diff(periods=1)
    _ohlcv["diff_up"] = np.where(_ohlcv["diff"] >= 0, _ohlcv["diff"], 0)
    _ohlcv["diff_down"] = np.where(_ohlcv["diff"] < 0, _ohlcv["diff"], 0)
    # Calculate Average Gain and Average Loss
    _ohlcv[["rsi_u", "rsi_d"]] = _ohlcv[["diff_up", "diff_down"]].ewm(alpha=1 / period, min_periods=period).mean()
    _ohlcv["rs"] = abs(_ohlcv["rsi_u"]) / abs(_ohlcv["rsi_d"])
    indicator_values = 100 - (100 / (1 + _ohlcv["rs"]))

    return indicator_values


def ADD_RSI():
    pass
    