from Import_price_data import *
from Indicators import *
from statsmodels.formula.api import ols

#Function to import the fama french three factor model data
def ff_3_factor_data():
	#Set start and end date - should be in line with the historical prices input
	end = dt.datetime.today()
	start = (dt.datetime.now() - dt.timedelta(days=1000)).strftime("%Y-%m-%d")
	ff_3_factor = web.DataReader('F-F_Research_Data_Factors_daily', 'famafrench', start, end)[0]
	ff_3_factor_df = pd.DataFrame(ff_3_factor)
	ff_3_factor_df = ff_3_factor_df.rename(columns = {"Mkt-RF": "Mkt_RF"})
	#FF_factors are given as percentages, divide by 100
	ff_3_factor_df[['Mkt_RF', 'SMB', 'HML', 'RF']] = ff_3_factor_df[['Mkt_RF', 'SMB', 'HML', 'RF']]/100

	return ff_3_factor_df


#Create a function to get the daily returns of the stock
def daily_lnRFreturns(df):
	ff_3_factor_df = ff_3_factor_data()
	DailyReturnsDF = pd.DataFrame()
	DailyReturnsDF['Close'] = df['Close']
	#Get the close price,less the risk free rate
	DailyReturnsDF['RFClose'] = DailyReturnsDF['Close'] - ff_3_factor_df['RF']
	#Normalize the RiskFree returns by getting the log difference
	DailyReturnsDF['ln_RFreturns'] = np.log(DailyReturnsDF['RFClose']) - np.log(DailyReturnsDF['RFClose'].shift(1))
	
	return(DailyReturnsDF,ff_3_factor_df)


#Create function to merge signals with the fama-french data
def merge_indicators_ff():
	BolingerBands_df = ISignals('BB')
	BolingerBands_df = BolingerBands_df.rename(columns={'Signal': 'BB_Signal'})
	BollingerBands_Signal = BolingerBands_df['BB_Signal']
	MACDdf = ISignals('MACD')
	MACDdf = MACDdf.rename(columns={'Signal': 'MACD_Signal'})
	MACD_Signal = MACDdf['MACD_Signal']
	RSIdf = ISignals('RSI')
	RSIdf = RSIdf.rename(columns={'Signal': 'RSI_Signal'})
	RSI_Signal = RSIdf['RSI_Signal']
	DailyReturnsDF, ff_3_factor_df = daily_lnRFreturns(df)
	#merge the indicators with the f-f dataframe
	ff_3_factor_1 = pd.merge(DailyReturnsDF, ff_3_factor_df, on = 'Date')
	ff_3_factor_2 = pd.merge(ff_3_factor_1, BollingerBands_Signal, on = 'Date')
	ff_3_factor_3 = pd.merge(ff_3_factor_2, MACD_Signal, on = 'Date')
	ff_3_factor_final = pd.merge(ff_3_factor_3, RSI_Signal, on = 'Date')
	ff_3_factor_final = ff_3_factor_final.dropna() #drop NA values

	return ff_3_factor_final


#Create a function to model indicator and FF3F
def FF3F(indicator):
	ff_3_factor_final = merge_indicators_ff()
	formula = f'ln_RFreturns ~ Mkt_RF + SMB + HML + {indicator}_Signal'
	FF3Fmodel = ols(formula = formula , data = ff_3_factor_final)
	FF3Fmodel_HAC = FF3Fmodel.fit(cov_type = 'HAC', cov_kwds = {'maxlags':None}, use_t=True)
	print(FF3Fmodel_HAC.summary())



FF3F('BB')
FF3F('MACD')
FF3F('RSI')