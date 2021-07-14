from Import_price_data import *

df = get_historical_prices("AAPL", "2y")
#Create a function to get the daily returns of the stock
def daily_returns(df):
	ff_3_factor_df = ff_3_factor_data()
	DailyReturnsDF = pd.DataFrame()
	DailyReturnsDF['Returns'] = df['Close'].pct_change()
	#Get the risk free rate
	DailyReturnsDF['RFreturns'] = DailyReturnsDF['Returns'] - ff_3_factor_df['RF']
	return DailyReturnsDF
	
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


daily_returns(df)