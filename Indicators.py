from Import_price_data import *

#Function from Import_price_data to create df of price
df = get_historical_prices("AAPL", "2y")

#Create a function to create Bollinger Bands dataframe. Takes in prices dataframe, returns dataframe
def BBandsDF(df):
	#TA-Lib to generate the bollinger bands
	upper, middle, lower = talib.BBANDS(df['Close'], matype = 0) #MA_Type.T3

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
	Signal = BBandsDF(df)
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
	Signal = MACDdf(df)
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
	Signal = RSIdf(df)
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
def ISignals(indicator):
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

	return Signal


#Create a function that plots the price and signal. Takes in the name of the indicator ('Indicator'), IndicatorDataFrame and displays a plot
def Plot_Price_Signal(Indicator, Signal):
	Indicator = Indicator
	Signal = Signal
	title = f'Close Price History Long/Short {Indicator} Signals'
	#Create and plot the graph
	plt.figure(figsize=(24,8)) #width = 24in, height = 8
	plt.scatter(Signal.index, Signal['Buy_Signal_Price'], color = 'green', label='Buy Signal', marker = '^', alpha = 1)
	plt.scatter(Signal.index, Signal['Sell_Signal_Price'], color = 'red', label='Sell Signal', marker = 'v', alpha = 1)
	plt.plot( Signal['Close'],  label='Close Price', alpha = 0.35)#plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)
	plt.xticks(rotation=45)
	plt.title(title)
	plt.xlabel('Date',fontsize=18)
	plt.ylabel('Close Price USD ($)',fontsize=18)
	plt.legend( loc='upper left')
	plt.show()


#Function to plot Bolinger bands indicator
def Plot_BollingerBands_Indicator():
	BBdf = BBandsDF(df)
	plt.title('Bollinger Bands')
	plt.figure(figsize=(24,8))
	plt.plot(BBdf['upper'], color = 'green', linewidth = .5, alpha = .75)
	plt.plot(BBdf['middle'], color = 'blue',linewidth = .5, alpha = .75)
	plt.plot(BBdf['lower'], color ='red', linewidth = .5, alpha = .75)
	plt.title('Bollinger Bands')
	plt.show()

#Create a function for the Bollinger Bands indicator
def BollingerBands():
	Signal = ISignals('BB')
	Plot_Price_Signal('Bollinger_Bands', Signal)

  
#Create a function for the MACD Indicator
def MACD():
	Signal = ISignals('MACD')
	Plot_Price_Signal('MACD', Signal)


#Create a function for the RSI Indicator
def RSI():
	Signal = ISignals('RSI')
	Plot_Price_Signal('RSI', Signal)


