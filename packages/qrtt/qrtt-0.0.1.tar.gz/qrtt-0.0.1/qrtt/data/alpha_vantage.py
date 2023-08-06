import pandas as pd


def load_daily(symbol="SPY", api_key='demo', start_date=None, end_date=None):
    try:
        file_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED' \
                   f'&symbol={symbol}' \
                   f'&apikey={api_key}' \
                   f'&datatype=csv' \
                   f'&outputsize=full'

        _df = pd.read_csv(file_url,
                          parse_dates=['timestamp'],
                          infer_datetime_format=True,
                          index_col='timestamp')

        _df = _df[['open', 'high', 'low', 'close', 'volume']]

        if start_date:
            _df = _df[_df.index >= start_date]
        if end_date:
            _df = _df[_df.index <= end_date]

        _df = _df.sort_index(ascending=True)

        return _df
    except Exception as e:
        print(f'An error occurred. \nError Message is {e}')
