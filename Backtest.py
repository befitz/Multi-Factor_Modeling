from Indicators import *
from Import_price_data import *

#Function to calculate the return for BollingerBands
def BollingerBands_BT(ticker, period):
	df = get_historical_prices(f"{ticker}", f"{period}")
	BBSignal = ISignals(df, 'BB')
	Sum_BuyPrice = BBSignal['Buy_Signal_Price'].sum()
	Sum_SellPrice = BBSignal['Sell_Signal_Price'].sum()
	Return = Sum_SellPrice - Sum_BuyPrice

	print(f"Using Bollinger Bands the return on {ticker} for {period} was:", Return, "per share")


#Function to calculate the return using MACD
def MACD_BT(ticker, period):
	df = get_historical_prices(f"{ticker}", f"{period}")
	MACDSignal = ISignals(df, 'MACD')
	Sum_BuyPrice = MACDSignal['Buy_Signal_Price'].sum()
	Sum_SellPrice = MACDSignal['Sell_Signal_Price'].sum()
	Return = Sum_SellPrice - Sum_BuyPrice

	print(f"Using MACD the return on {ticker} for {period} was:", Return, "per share")


#Function to calculate the return using RSI
def RSI_BT(ticker, period):
	df = get_historical_prices(f"{ticker}", f"{period}")
	RSISignal = ISignals(df, 'RSI')
	Sum_BuyPrice = RSISignal['Buy_Signal_Price'].sum()
	Sum_SellPrice = RSISignal['Sell_Signal_Price'].sum()
	Return = Sum_SellPrice - Sum_BuyPrice

	print(f"Using RSI the return on {ticker} for {period} was:", Return, "per share")


def test_all(ticker, period):
	BollingerBands_BT(f"{ticker}", f"{period}")
	MACD_BT(f"{ticker}", f"{period}")
	RSI_BT(f"{ticker}", f"{period}")



test_all('AMC', '6mo')