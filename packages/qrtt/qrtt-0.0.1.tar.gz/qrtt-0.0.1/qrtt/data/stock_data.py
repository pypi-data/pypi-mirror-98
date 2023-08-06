import pandas as pd
import numpy as np

def load_historical(symbol="SPY",
                    frequency='daily',
                    locale='us',
                    start_date=None,
                    end_date=None):

    try:
        file_url = f'https://data.qrtt.org/equity/{locale}/historical/{frequency}/{symbol}.csv'
        _df = pd.read_csv(file_url,
                          parse_dates=['timestamp'],
                          infer_datetime_format=True,
                          index_col='timestamp')
        # _df.index = _df.index.tz_localize(None)
        if start_date:
            _df = _df[_df.index >= start_date]
        if end_date:
            _df = _df[_df.index <= end_date]
        return _df
    except Exception as e:
        print(f'An error occurred. \nError Message is {e}')
