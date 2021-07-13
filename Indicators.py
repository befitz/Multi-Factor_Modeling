from Import_price_data import *

#Create a function to create Bollinger Bands dataframe. Takes in prices dataframe, returns dataframe
def BBandsDF(df):
	#TA-Lib to generate the bollinger bands
	upper, middle, lower = talib.BBANDS(df['Close'], matype=MA_Type.T3)
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
  flag = 0
  sig = []
  sigPriceBuy = []
  sigPriceSell = []
  for i in range(0,len(BBdf)):
    #if price is > upper then sell
      if BBdf['Close'][i] > BBdf['upper'][i]:
        if flag != 1:
          sigPriceBuy.append(BBdf['Close'][i])
          sigPriceSell.append(np.nan)
          sig.append(1)
          flag = 1
        else:
          sigPriceBuy.append(np.nan)
          sigPriceSell.append(np.nan)
          sig.append(1)
          flag = 1
      #if price is < lower then sell
      elif BBdf['Close'][i] < BBdf['lower'][i]: 
        if flag != 0:
          sigPriceSell.append(BBdf['Close'][i])
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
  flag = 0
  sig = []
  sigPriceBuy = []
  sigPriceSell = []
  for i in range(0,len(MACDdf)):
    #if MACD > signal line  then buy else sell
      if MACDdf['macd'][i] > MACDdf['macdsignal'][i]:
        if flag != 1:
          sigPriceBuy.append(MACDdf['Close'][i])
          sigPriceSell.append(np.nan)
          sig.append(1)
          flag = 1
        else:
          sigPriceBuy.append(np.nan)
          sigPriceSell.append(np.nan)
          sig.append(1)
          flag = 1
      elif MACDdf['macd'][i] < MACDdf['macdsignal'][i]: 
        if flag != 0:
          sigPriceSell.append(MACDdf['Close'][i])
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
  flag = 0
  sig = []
  rsiSigPriceBuy = []
  rsiSigPriceSell = []
  for i in range(0,len(signal)):
    #if RSI > 0.30  then buy else sell
      if RSIdf['rsi'][i-1] <= 0.30:
        if RSIdf['rsi'][i] >= 0.30:
          if flag == 0:
            rsiSigPriceBuy.append(RSIdf['Close'][i])
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
      elif RSIdf['rsi'][i-1] >= 0.70:
        if RSIdf['rsi'][i] <= 0.70:
          if flag == 0:
            rsiSigPriceBuy.append(np.NaN)
            rsiSigPriceSell.append(np.NaN)
            sig.append(0)
            flag = 0
          else:
            rsiSigPriceBuy.append(np.NaN)
            rsiSigPriceSell.append(RSIdf['Close'][i])
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
def ISignals(Signal, IndicatorDataFrame):
	IndicatorDataFrame['Buy_Signal_Price'] = Signal[0]
	IndicatorDataFrame['Sell_Signal_Price'] = Signal[1]
	IndicatorDataFrame['Signal'] = Signal[2]

	return IndicatorDataFrame


#Create a function that plots the price and signal. Takes in the name of the indicator ('Indicator'), IndicatorDataFrame and displays a plot
def Plot_Price_Signal(Indicator, IndicatorDataFrame):
	Indicator = Indicator
	title = f'Close Price History Long/Short {Indicator} Signals'
	#Create and plot the graph
	plt.figure(figsize=(24,8)) #width = 24in, height = 8
	plt.scatter(IndicatorDataFrame.index, IndicatorDataFrame['Buy_Signal_Price'], color = 'green', label='Buy Signal', marker = '^', alpha = 1)
	plt.scatter(IndicatorDataFrame.index, IndicatorDataFrame['Sell_Signal_Price'], color = 'red', label='Sell Signal', marker = 'v', alpha = 1)
	plt.plot( IndicatorDataFrame['Close'],  label='Close Price', alpha = 0.35)#plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)
	plt.xticks(rotation=45)
	plt.title(title)
	plt.xlabel('Date',fontsize=18)
	plt.ylabel('Close Price USD ($)',fontsize=18)
	plt.legend( loc='upper left')
	plt.show()


#Create a function for the Bollinger Bands indicator
def BollingerBands():
	#Function for the ta-lib calc
	Signal = BBandsDF(df)
	#Function for the Indicators
	IndicatorDataFrame = BBbuy_sell(Signal)
	BollingerBandsFinal = ISignals(Signal, IndicatorDataFrame)
	Plot_Price_Signal('Bollinger_Bands', BollingerBandsFinal)

#Create a function for the MACD Indicator
def MACD():
	Signal = MACDdf(df)
	IndicatorDataFrame = MACDbuy_sell(Signal)
	MACDFinal = ISignals(Signal, IndicatorDataFrame)
	Plot_Price_Signal('MACD', MACDFinal)


#Create a function for the RSI Indicator
def RSI():
	Signal = RSIdf(df)
	IndicatorDataFrame = RSIbuy_sell(Signal)
	RSIFinal = ISignals(Signal,IndicatorDataFrame)
	Plot_Price_Signal('RSI', RSIFinal)


BollingerBands()
MACD()
RSI()
