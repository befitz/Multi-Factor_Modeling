from Import_price_data import *
from talib import MA_Type

#Create a function to build a dataframe for Simple Moving Average 200 days
def SimpleMAdf(df):
	SMA = talib.SMA(df['Close'].values, timeperiod = 180)
	SMAdf = pd.DataFrame()
	SMAdf['Close'] = df['Close']
	SMAdf['SMA'] = SMA

	return SMAdf

#Create a function to create Bollinger Bands dataframe. Takes in prices dataframe, returns dataframe
def BBandsDF(df):
	#TA-Lib to generate the bollinger bands
	upper, middle, lower = talib.BBANDS(df['Close'], nbdevup=2, nbdevdn=2, matype = MA_Type.T3) #MA_Type.T3

	#Build the DataFrame
	BBdf = pd.DataFrame()
	BBdf['upper'] = upper
	BBdf['middle'] = middle
	BBdf['lower'] = lower
	BBdf['Close'] = df['Close']
	BBdf = BBdf.dropna()

	return BBdf

#Create a function to create a MACD dataframe and signal line. Takes in prices dataframe, returns dataframe
def MACDdf(df):
	#TA-Lib to generate the MACD lines
	macd, macdsignal, macdhist = talib.MACD(df['CloseLag1'], fastperiod=9, slowperiod=26, signalperiod=7)

	MACDdf = pd.DataFrame()
	MACDdf['macd'] = macd
	MACDdf['macdsignal'] = macdsignal
	MACDdf['macdhist'] = macdhist
	MACDdf['Close'] = df['Close']
	MACDdf = MACDdf.dropna()

	return MACDdf


#Create a function to make an RSI dataframe and signal line. Takes in prices dataframe, returns dataframe
def RSIdf(df):
	#TA-Lib to generate the RSI lines
	rsi = talib.RSI(df['Close'],timeperiod=9)/100
	RSIdf = pd.DataFrame()
	RSIdf['rsi'] = rsi
	RSIdf['Close'] = df['Close']
	RSIdf = RSIdf.dropna()

	return RSIdf


#Create a function to signal when to buy/sell/hold
#Long and hold will be 1
#Short will be 0
def BBbuy_sell(signal):
	Signal = signal
	flag = 0
	sig = []
	sigPriceBuy = []
	sigPriceSell = []
	for i in range(0,len(Signal)):
	#if price is > upper then sell
	  if Signal['Close'][i] > Signal['upper'][i]:
	    if flag != 1:
	      sigPriceBuy.append(Signal['Close'][i])
	      sigPriceSell.append(np.nan)
	      sig.append(1)
	      flag = 1
	    else:
	      sigPriceBuy.append(np.nan)
	      sigPriceSell.append(np.nan)
	      sig.append(1)
	      flag = 1
	  #if price is < lower then sell
	  elif Signal['Close'][i] < Signal['lower'][i]: 
	    if flag != 0:
	      sigPriceSell.append(Signal['Close'][i])
	      sigPriceBuy.append(np.nan)
	      sig.append(0)
	      flag = 0
	    else:
	      sigPriceSell.append(np.nan)
	      sigPriceBuy.append(np.nan)
	      sig.append(0)
	      flag = 0
	  else: #Handling nan values
	    sigPriceSell.append(np.nan)
	    sigPriceBuy.append(np.nan)
	    sig.append(0)

	return (sigPriceBuy, sigPriceSell, sig)
	del (sigPriceBuy, sigPriceSell, sig)


#Create a function to signal when to buy/sell/hold
#Long and hold will be 1
#Short will be 0
def MACDbuy_sell(signal):
	Signal = signal
	flag = 0
	sig = []
	sigPriceBuy = []
	sigPriceSell = []
	for i in range(0,len(Signal)):
    #if MACD > signal line  then buy else sell
		if Signal['macd'][i] > Signal['macdsignal'][i]:
			if flag != 1:
			  sigPriceBuy.append(Signal['Close'][i])
			  sigPriceSell.append(np.nan)
			  sig.append(1)
			  flag = 1
			else:
			  sigPriceBuy.append(np.nan)
			  sigPriceSell.append(np.nan)
			  sig.append(1)
			  flag = 1
		elif Signal['macd'][i] < Signal['macdsignal'][i]: 
			if flag != 0:
			  sigPriceSell.append(Signal['Close'][i])
			  sigPriceBuy.append(np.nan)
			  sig.append(0)
			  flag = 0
			else:
			  sigPriceSell.append(np.nan)
			  sigPriceBuy.append(np.nan)
			  sig.append(0)
			  flag = 0
		else: #Handling nan values
			sigPriceSell.append(np.nan)
			sigPriceBuy.append(np.nan)
			sig.append(0)

	return (sigPriceBuy, sigPriceSell, sig)
	del (sigPriceBuy, sigPriceSell, sig)


#Create a function to signal when to buy/sell/hold
#signal: pandas.DataFrame including rsi and close price
#Returns: lists
#Long and hold will be 1
#Short will be 0
def RSIbuy_sell(signal):
	Signal = signal
	flag = 0
	sig = []
	rsiSigPriceBuy = []
	rsiSigPriceSell = []
	for i in range(0,len(Signal)):

    #if RSI > 0.30  then buy else sell
		if Signal['rsi'][i-1] <= 0.30:
			if Signal['rsi'][i] >= 0.30:
			  if flag == 0:
			    rsiSigPriceBuy.append(Signal['Close'][i])
			    rsiSigPriceSell.append(np.NaN)
			    sig.append(1)
			    flag = 1
			  else:
			    rsiSigPriceBuy.append(np.NaN)
			    rsiSigPriceSell.append(np.NaN)
			    sig.append(1)
			    flag = 1
			else:
			  rsiSigPriceBuy.append(np.NaN)
			  rsiSigPriceSell.append(np.NaN)
			  sig.append(flag)
			  flag = flag
		elif Signal['rsi'][i-1] >= 0.70:
			if Signal['rsi'][i] <= 0.70:
			  if flag == 0:
			    rsiSigPriceBuy.append(np.NaN)
			    rsiSigPriceSell.append(np.NaN)
			    sig.append(0)
			    flag = 0
			  else:
			    rsiSigPriceBuy.append(np.NaN)
			    rsiSigPriceSell.append(Signal['Close'][i])
			    sig.append(0)
			    flag = 0
			else:
			  rsiSigPriceBuy.append(np.NaN)
			  rsiSigPriceSell.append(np.NaN)
			  sig.append(flag)
			  flag = flag
		else: #Handling nan values
			rsiSigPriceBuy.append(np.NaN)
			rsiSigPriceSell.append(np.NaN)
			sig.append(flag)
      
	return (rsiSigPriceBuy, rsiSigPriceSell, sig)


#Create function to create signal columns for buy/sell and signals of the indicator. Takes in signal and indicator, returns indicator dataframe with signals
#IndicatorDataFrame is the result of the function that creates the indicator
#Signal is the result of the *buy_sell(*df) input
#indicator is BB,MACD, or RSI
def ISignals(df, indicator):
	#Function for the simple-moving-average 200 day
	SMA = SimpleMAdf(df)
	if indicator == 'BB':
		#Function for the ta-lib calc
		Signal = BBandsDF(df)
		#Function for the Indicators
		IndicatorDataFrame = BBbuy_sell(Signal)
	elif indicator == 'MACD':
		Signal = MACDdf(df)
		IndicatorDataFrame = MACDbuy_sell(Signal)
	elif indicator == 'RSI':
		Signal = RSIdf(df)
		IndicatorDataFrame = RSIbuy_sell(Signal)
	Signal['Buy_Signal_Price'] = IndicatorDataFrame[0]
	Signal['Sell_Signal_Price'] = IndicatorDataFrame[1]
	Signal['Signal'] = IndicatorDataFrame[2]
	Signal['SMA'] = SMA['SMA']

	return Signal


#Create a function to display 2 plots, one for the buy/sell signal and one for the indicator lines
def Plot_Single_Indicator_Signals(Indicator, ticker, start_date):
	df = get_historical_prices(f"{ticker}", "1y")
	df = df.loc[f'{start_date}':]
	Indicator = Indicator
	Signal = ISignals(df, f'{Indicator}')
	fig, (ax0, ax1) = plt.subplots(2, 1, sharex = True, figsize= (24,8))
	ax0.plot(Signal.index, Signal['Close'], alpha = .75, linewidth = 2, color = 'k')
	ax0.plot(Signal.index, Signal['SMA'], alpha = .75, linewidth = 1, color = 'b')
	ax0.scatter(Signal.index, Signal['Buy_Signal_Price'], color = 'green', label='Buy Signal', marker = '^', alpha = 1)
	ax0.scatter(Signal.index, Signal['Sell_Signal_Price'], color = 'red', label='Sell Signal', marker = 'v', alpha = 1)
	ax0.set_xlabel('Date',fontsize=12)
	ax0.set_ylabel('Close Price USD ($)',fontsize=18)
	ax0.grid(True)
	
	if Indicator == 'BB':
		BBdf = BBandsDF(df)
		ax1.plot(BBdf['upper'], color = 'green', linewidth = .5, alpha = .75)
		ax1.plot(BBdf['middle'], color = 'blue',linewidth = .5, alpha = .75)
		ax1.plot(BBdf['lower'], color ='red', linewidth = .5, alpha = .75)
	elif Indicator == 'MACD':
		MACD_df = MACDdf(df)
		ax1.plot(MACD_df['macd'], label = 'MACD', linewidth = .75, alpha = .75)
		ax1.plot(MACD_df['macdsignal'], label = 'Signal', linewidth = .75, alpha = .75)
	elif Indicator == 'RSI':
		RSI_df = RSIdf(df)
		ax1.plot(RSI_df['rsi'])
		ax1.axhline(0, linestyle = '--', alpha = 0.5, color='gray')
		ax1.axhline(.10, linestyle = '--', alpha = 0.5, color='orange')
		ax1.axhline(.20, linestyle = '--', alpha = 0.5, color='green')
		ax1.axhline(.30, linestyle = '--', alpha = 0.5, color='red')
		ax1.axhline(.70, linestyle = '--', alpha = 0.5, color='red')
		ax1.axhline(.80, linestyle = '--', alpha = 0.5, color='green')
		ax1.axhline(.90, linestyle = '--', alpha = 0.5, color='orange')
		ax1.axhline(1, linestyle = '--', alpha = 0.5, color='gray')
	
	ax1.set_xlabel('Date', fontsize = 12)
	ax1.set_ylabel(f'{Indicator}')
	ax1.grid(True)

	fig.tight_layout()
	plt.show()


#Function to display all indicators start_date format yyyy-mm-dd
def Plot_All_Indicator_Signals(ticker, start_date):
	df = get_historical_prices(f"{ticker}", "1y")
	SMASignal = SimpleMAdf(df)
	SMASignal = SMASignal.loc[f'{start_date}':]
	BBSignal = ISignals(df, 'BB')
	BBSignal = BBSignal.loc[f'{start_date}':]
	MACDSignal = ISignals(df, 'MACD')
	MACDSignal = MACDSignal.loc[f'{start_date}':]
	RSISignal = ISignals(df, 'RSI')
	RSISignal = RSISignal.loc[f'{start_date}':]
	#Plot the SMA and closing price of the stock
	fig, (ax0, ax1, ax2, ax3) = plt.subplots(4, 1, sharex = True, figsize= (24,10))
	ax0.plot(SMASignal.index, SMASignal['Close'], alpha = .75, linewidth = 1, color = 'k', label = 'Close Price $')
	ax0.plot(SMASignal.index, SMASignal['SMA'], alpha = .75, linewidth = 1, color = 'b', label = 'Simple Moving Average (180 days)')
	#using ^ and v to note buys and sells
	ax0.scatter(BBSignal.index, BBSignal['Buy_Signal_Price'], s=75, color = 'green', label='Buy Signal', marker = '^', alpha = .5)
	ax0.scatter(BBSignal.index, BBSignal['Sell_Signal_Price'], s=75, color = 'red', label='Sell Signal', marker = 'v', alpha = .5)
	ax0.scatter(MACDSignal.index, MACDSignal['Buy_Signal_Price'], s = 75, color = 'green', marker = '^', alpha = .5)
	ax0.scatter(MACDSignal.index, MACDSignal['Sell_Signal_Price'], s=75, color = 'red', marker = 'v', alpha = .5)
	ax0.scatter(RSISignal.index, RSISignal['Buy_Signal_Price'], s=75, color = 'green', marker = '^', alpha = .5)
	ax0.scatter(RSISignal.index, RSISignal['Sell_Signal_Price'], s=75, color = 'red', marker = 'v', alpha = .5)
	ax0.set_ylabel('Close Price USD ($)',fontsize=18)
	ax0.legend(loc=0, fontsize=10)
	ax0.grid(True)
	#Plot bollinger band lines with closing price
	BBdf = BBandsDF(df)
	BBdf = BBdf.loc[f'{start_date}':]
	ax1.plot(BBdf['upper'], color = 'green', linewidth = .75, alpha = .75, label = 'Upper Band')
	ax1.plot(BBdf['middle'], color = 'blue',linewidth = .75, alpha = .75, label = 'Middle Band')
	ax1.plot(BBdf['lower'], color ='red', linewidth = .75, alpha = .75, label= 'Lower Band')
	ax1.plot(SMASignal.index, SMASignal['Close'], alpha = .75, linewidth = 1.25, color ='k', label = 'Close Price $')
	ax1.set_ylabel('Bollinger Bands')
	ax1.legend(loc=0, fontsize=10)
	ax1.grid(True)
	#Plot MACD lines
	MACD_df = MACDdf(df)
	MACD_df = MACD_df.loc[f'{start_date}':]
	ax2.plot(MACD_df['macd'], label = 'MACD', linewidth = .75, alpha = .75)
	ax2.plot(MACD_df['macdsignal'], label = 'MACD Signal', linewidth = .75, alpha = .75)
	ax2.set_ylabel('MACD')
	ax2.legend(loc=0, fontsize=10)
	ax2.grid(True)
	#Plot RSI line and line idicators for 0-100%
	RSI_df = RSIdf(df)
	RSI_df = RSI_df.loc['2021-07-12':]
	ax3.plot(RSI_df['rsi'], label = 'RSI', linewidth=1.5, alpha=1)
	ax3.axhline(0, linestyle = '--', alpha = 0.5, linewidth=.75, color='gray')
	ax3.axhline(.10, linestyle = '--', alpha = 0.5, linewidth=.75, color='orange')
	ax3.axhline(.20, linestyle = '--', alpha = 0.5, linewidth=.75, color='green')
	ax3.axhline(.30, linestyle = '--', alpha = 0.5, linewidth=.75, color='red')
	ax3.axhline(.70, linestyle = '--', alpha = 0.5, linewidth=.75, color='red')
	ax3.axhline(.80, linestyle = '--', alpha = 0.5, linewidth=.75, color='green')
	ax3.axhline(.90, linestyle = '--', alpha = 0.5, linewidth=.75, color='orange')
	ax3.axhline(1, linestyle = '--', alpha = 0.5, linewidth=.75, color='gray')
	ax3.set_xlabel('Date', fontsize = 12)
	ax3.set_ylabel('RSI')
	ax3.legend(loc=0, fontsize=10)
	ax3.grid(True)

	fig.tight_layout()
	plt.show()


