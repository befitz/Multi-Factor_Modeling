import pandas_datareader.data as pdr
from pandas_datareader import DataReader
from pandas_datareader import data as web
import talib
import pandas as pd
import numpy as np
import datetime as dt
import seaborn as sns
import statsmodels.api as smf
import math
import pandas.util.testing as tm
import matplotlib.pyplot as plt
import yfinance as yf



plt.style.use('fivethirtyeight')

#Set start/end dates to pull historic price data
end = dt.datetime.today().strftime("%Y-%m-%d")
start = (dt.datetime.now() - dt.timedelta(days=360)).strftime("%Y-%m-%d")
#ticker = input("Ticker:")
ticker = 'AAPL'
#Request historic price data from pandas datareader
df = web.DataReader(f'{ticker}', data_source='yahoo', start=start)

#Create Lags
df['CloseLag1'] = df['Adj Close'].shift(-1)
df['CloseLag2'] = df['Adj Close'].shift(-2)
df['Close'] = df['Adj Close']