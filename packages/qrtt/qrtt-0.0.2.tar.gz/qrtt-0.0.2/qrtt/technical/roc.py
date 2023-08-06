# Rate of Change (RoC)

def roc(ohlcv, period=1, ohlcv_series="close"):
    """
    CALCULATION
    ROC = ( Current Price - Price N periods ago ) / Price N periods ago
    """
    _ohlcv = ohlcv[[ohlcv_series]].copy(deep=True)
    indicator_values = _ohlcv[ohlcv_series].pct_change(period)
    return indicator_values
