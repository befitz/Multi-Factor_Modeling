import talib
from pandas_datareader import DataReader
from pandas_datareader import data as web
import pandas as pd
import numpy as np
import datetime as dt
import seaborn as sns
import statsmodels.api as smf
import math
import pandas.util.testing as tm
import matplotlib.pyplot as plt
%matplotlib inline
plt.style.use('fivethirtyeight')

#Set start/end dates to pull historic price data
end = dt.datetime.today()
start = (dt.datetime.now() - dt.timedelta(days=6000)).strftime("%m-%d-%Y")

ticker = 'UPST'
#Request historic price data from pandas datareader
df = web.DataReader(f'{ticker}', data_source='yahoo', start=start)

#Create Lags
df['CloseLag1'] = df['Adj Close'].shift(-1)
df['CloseLag2'] = df['Adj Close'].shift(-2)
df['Close'] = df['Adj Close']