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



#function to take in a ticker and period (1mo, 1y, 3y etc.) and return dataframe
def get_historical_prices(ticker, period):
	ticker = yf.Ticker(f"{ticker}")
	df = ticker.history(period=f"{period}")
	#Create Lags
	df['CloseLag1'] = df['Close'].shift(-1)
	df['CloseLag2'] = df['Close'].shift(-2)

	return df

