# Standard MACD function
def macd(ohlcv, short_period=12, long_period=26, signal_period=9, ohlcv_series="close"):
    """
    DESCRIPTION

    Gerald Appel developed Moving Average Convergence/Divergence as an indicator
    of the change in a security's underlying price trend. The theory suggests that
    when a price is trending, it is expected, from time to time, that speculative
    forces "test" the trend.  MACD shows characteristics of both a trending indicator
    and an oscillator. While the primary function is to identify turning points in a
    trend, the level at which the signals occur determines the strength of the reading.

    CALCULATION

    MACD Line:
     MACD=Period1 Exponential MA (Fast) -
          Period2 Exponential MA (Slow)
    MACD Signal Line:
     Sig=Period3 Exponential MA of MACD Line
    MACD Diff:
     Diff=MACD - Sig

    where:
    Period1 = N Period of the Fast Exponential MA
     The default Period1 is 12
    Period2 = N Period of the Slow Exponential MA
     The default Period2 is 26
    Period3 = N Period Exponential MA for the Signal Line
     The default Period3 is 9
    MACD Period:
     N Period = For daily, N=days; weekly, N=weeks, ...
    MACD omits non-trading days from computations.

    Formula:
    MACD Line: (12-day EMA - 26-day EMA)
    Signal Line: 9-day EMA of MACD Line
    MACD Histogram: MACD Line - Signal Line

    Validation: validated with results from Bloomberg
    """
    _ohlcv = ohlcv[[ohlcv_series]].copy(deep=True)
    _ohlcv["short"] = _ohlcv[ohlcv_series].ewm(span=short_period, min_periods=short_period).mean()
    _ohlcv["long"] = _ohlcv[ohlcv_series].ewm(span=long_period, min_periods=long_period).mean()
    _ohlcv["macd"] = _ohlcv["short"] - _ohlcv["long"]
    _ohlcv["signal"] = _ohlcv["macd"].ewm(span=signal_period, min_periods=signal_period).mean()
    _ohlcv["hist"] = _ohlcv["macd"] - _ohlcv["signal"]

    return _ohlcv[["macd", "signal", "hist"]]