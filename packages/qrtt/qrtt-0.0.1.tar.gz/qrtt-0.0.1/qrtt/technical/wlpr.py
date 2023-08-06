# William %R

"""
WLPR allows you to plot the Williams %R value for a selected security.
It is useful in recognizing potential turning points to help make entry/exit
decisions and display event tracks. Use WLPR to determine overbought/oversold
levels: the Williams %R oscillator identifies whether a security is trading
at a relative high or low in relation to the highs and lows of a look back
period based on selected periodicity.  The default period for the indicator
is 14 periods for all chart types; intraday, daily, weekly, monthly.

WLPR Calculation

WLPR=-100*(N Period Highest High - Close) /
          (N Period Highest High - N Period Lowest Low)

where:
Highest High=The highest High over the specified N Period.
Lowest Low  =The lowest Low over the specified N Period.
N Period = For daily, N=days; weekly, N=weeks, ...
 The default is 14

WLPR omits non-trading days from computations.


"""

def wlpr(ohlcv, period=14, ohlcv_series="close"):
    """
    VALIDATION: validated with results from Bloomberg and TradingView
    """
    _ohlcv = ohlcv[['high', 'low', ohlcv_series]].copy(deep=True)
    _ohlcv['n_high'] = _ohlcv['high'].rolling(window=period, min_periods=period).max()
    _ohlcv['n_low'] = _ohlcv['low'].rolling(window=period, min_periods=period).min()

    indicator_values = -100 * (_ohlcv['n_high'] - _ohlcv[ohlcv_series]) / (_ohlcv['n_high'] - _ohlcv['n_low'])
    return indicator_values
