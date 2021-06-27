import concurrent
import pandas as pd
from pandas_datareader import data
# get historical stock data from yahoo finance
import numpy as np
from base import cache
import os
import datetime

def collect_stocks_data(tickers, end=None, days=None):
    end = datetime.datetime.now() if end is None else end
    start = end - datetime.timedelta(days=365 if days is None else days)
    with concurrent.futures.ThreadPoolExecutor(os.cpu_count() + 1) as executor:
        result = list(executor.map(lambda t: get_historical_data(t, start, end), tickers))
    executor.shutdown(wait=True)
    return_df = pd.DataFrame([r[0] for r in result]).T
    price_df = pd.DataFrame([r[1] for r in result]).T
    return_df.columns, price_df.columns = tickers, tickers
    return return_df, price_df


def get_historical_data(ticker, start, end):
    """
    :param ticker: Ticker of a stock (str)
    :param start: start date of the historical data (datetime)
    :param end: end date of the historical data (datetime)
    :return: (daily return, daily adj close price)
    """
    df = cache.get('ticker')
    if df is not None:
        return df
    try:
        df = data.DataReader(ticker, start=start, end=end, data_source='yahoo')
        df = df[['Adj Close']]
        clean_data(df)
        df['return'] = np.log(df['Adj Close'].pct_change() + 1)
        return df['return'].dropna(), df['Adj Close']
    except:
        raise Exception("Failed to collect data for {}".format(ticker))

# use last good value to replace Nan
# This method mutate the given df
def clean_data(df):
    """
    :param df: a DataFrame which contains historical data of a stock
    """
    df.fillna(method='ffill', inplace=True)