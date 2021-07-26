from Indicators import *
from Import_price_data import *


#Function to get the most recent closing price
def get_current_price(symbol):
	ticker = yf.Ticker(symbol)
	latest_price = ticker.history(period='1d')

	return latest_price['Close'][0]


#Function to calculate the return for BollingerBands
def BollingerBands_BT(ticker, start_date, latest_price):
	df = get_historical_prices(f"{ticker}", "1y")
	df = df.loc[f'{start_date}':]
	BBSignal = ISignals(df, 'BB')
	Sum_BuyPrice = BBSignal['Buy_Signal_Price'].sum()
	Sum_SellPrice = BBSignal['Sell_Signal_Price'].sum()
	#check if holding or if all position has sold
	if BBSignal['Signal'][-1] != 1:
		Return = Sum_SellPrice - Sum_BuyPrice
	else:
		Return = latest_price - Sum_BuyPrice

	print(f"Using Bollinger Bands the return on {ticker} if bought on {start_date} was:", Return, "per share")


#Function to calculate the return using MACD
def MACD_BT(ticker, start_date, latest_price):
	df = get_historical_prices(f"{ticker}", "1y")
	df = df.loc[f'{start_date}':]
	MACDSignal = ISignals(df, 'MACD')
	Sum_BuyPrice = MACDSignal['Buy_Signal_Price'].sum()
	Sum_SellPrice = MACDSignal['Sell_Signal_Price'].sum()
	if MACDSignal['Signal'][-1] != 1:
		Return = Sum_SellPrice - Sum_BuyPrice
	else:
		Return = latest_price - Sum_BuyPrice

	print(f"Using MACD the return on {ticker} if bought on {start_date} was:", Return, "per share")


#Function to calculate start_date return using RSI
def RSI_BT(ticker, start_date, latest_price):
	df = get_historical_prices(f"{ticker}", "1y")
	df = df.loc[f'{start_date}':]
	RSISignal = ISignals(df, 'RSI')
	Sum_BuyPrice = RSISignal['Buy_Signal_Price'].sum()
	Sum_SellPrice = RSISignal['Sell_Signal_Price'].sum()
	if RSISignal['Signal'][-1] != 1:
		Return = Sum_SellPrice - Sum_BuyPrice
	else:
		Return = latest_price - Sum_BuyPrice

	print(f"Using RSI the return on {ticker} bought on {start_date} was:", Return, "per share")


def test_all(ticker, start_date):
	latest_price = get_current_price(f'{ticker}')
	BollingerBands_BT(f"{ticker}", f"{start_date}", latest_price)
	MACD_BT(f"{ticker}", f"{start_date}", latest_price)
	RSI_BT(f"{ticker}", f"{start_date}", latest_price)



#Plot_All_Indicator_Signals('BX', '2021-06-01')
#test_all('BX', '2021-06-01')
Plot_Single_Indicator_Signals('BB', 'BX', '2021-06-01')