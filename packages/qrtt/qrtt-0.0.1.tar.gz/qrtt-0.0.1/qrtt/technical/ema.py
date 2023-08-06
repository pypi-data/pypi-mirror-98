
def ema(ohlcv, period=10, ohlcv_series="close"):
    """

    Validation: verified with numbers from TradingView
    """
    _ohlcv = ohlcv[[ohlcv_series]].copy(deep=True)
    indicator_values = _ohlcv[ohlcv_series].ewm(span=period, min_periods=period).mean()
    return indicator_values
