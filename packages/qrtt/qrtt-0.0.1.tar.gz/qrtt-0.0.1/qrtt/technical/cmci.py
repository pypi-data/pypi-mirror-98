"""
The Commodity Channel Index (CMCI), developed by Donald Lambert,
measures the variation of a security's price from its statistical mean.

The CMCI can be used to identify possible divergences that may indicate
a forthcoming trend for a selected security. A CMCI indicator falling
below a value of -100 indicates an oversold condition. A buy signal is
triggered when the indicator crosses -100 from below. Similarly, a CCI
value greater than 100 indicates an overbought condition. A sell signal
is triggered when the indicator crosses 100 from above.

CMCI Calculations
CMCI=(HLC3 - N Period Simple MA of HLC3) /
     (0.015 * N Period Mean Deviation of HLC3)

where:
HLC3 = (High + Low + Close) / 3
N Period= Number of data points to use;

"""
import numpy as np


def cmci(ohlcv, period=13):
    """
    VALIDATION

    Results are similar to Bloomberg data to the 4th digit after the decimal point.
    But very different from TradingView data.
    In some formulas, high and low are the highs and lows of the past N days.
    """
    _ohlcv = ohlcv[['high', 'low', 'close']].copy(deep=True)
    _ohlcv['hlc3'] = _ohlcv[['high', 'low', 'close']].mean(axis=1)
    _ohlcv['hlc3_ma'] = _ohlcv['hlc3'].rolling(window=period, min_periods=period).mean()
    _ohlcv['hlc3_mad'] = _ohlcv['hlc3'].rolling(window=period, min_periods=period).apply(
        lambda x: np.fabs(x - x.mean()).mean())

    indicator_values = (_ohlcv['hlc3'] - _ohlcv['hlc3_ma']) / (0.015 * _ohlcv['hlc3_mad'])
    return indicator_values
