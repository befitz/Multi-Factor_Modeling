import yfinance as yf
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
plt.style.use('fivethirtyeight')

ticker = 'AAPL'

#Request historic price data from yfinance

df = ticker.history(period="2y")

#Create Lags
df['CloseLag1'] = df['Close'].shift(-1)
df['CloseLag2'] = df['Close'].shift(-2)
