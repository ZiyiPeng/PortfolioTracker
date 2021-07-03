import concurrent
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import numpy as np
from base import cache
import os
import datetime
from python.model.stock import Stock
yf.pdr_override()

def collect_stocks_data(tickers, end=None, days=None):
    end = datetime.datetime.now() if end is None else end
    start = end - datetime.timedelta(days=365 if days is None else days)
    # with concurrent.futures.ThreadPoolExecutor(os.cpu_count() + 1) as executor:
    #     result = list(executor.map(lambda t: get_historical_data(t, start, end), tickers))
    # executor.shutdown(wait=True)
    result = list(map(lambda t: get_historical_data(t, start, end), tickers))
    return_df = pd.DataFrame([r[0] for r in result]).T
    price_df = pd.DataFrame([r[1] for r in result]).T
    return_df.columns, price_df.columns = tickers, tickers
    return return_df, price_df

def collect_stock_info(tickers):
    stocks = Stock.get_stocks(tickers)
    result = {s.ticker: {'industry': s.industry, 'sector': s.sector} for s in stocks}
    return result


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
        df = pdr.get_data_yahoo(ticker, start=start, end=end)
        df = df[['Adj Close']].fillna(method='ffill')
        df['return'] = np.log(df['Adj Close'].pct_change() + 1)
        return df['return'].dropna(), df['Adj Close']
    except:
        raise Exception("Failed to collect data for {}".format(ticker))
