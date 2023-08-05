import pandas as pd
import numpy as np
from pytickersymbols import PyTickerSymbols
from datetime import datetime
import pandas_datareader as pdr


class Backtest:
    def __init__(self, stock_index = "CAC 40", start_date = None, end_date = None, path_to_data = None):
        self.stock_index = stock_index
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.informations = None
        self.stock_index_tickers = {"CAC 40":"^FCHI","BEL 20":"^BFX", "S&P 500":"^GSPC"}
        self.returns = None #on the period
        self.daily_returns = None #daily
        self.path_to_data = path_to_data
        self.summary = None
        
    def load_data(self):
        if self.path_to_data:
            self.data = pd.read_csv(self.path_to_data, parse_dates =True, index_col=0)
        else:
            stock_data = PyTickerSymbols()
            stock_index = stock_data.get_stocks_by_index(self.stock_index)
            stocks_ticker = [self.stock_index_tickers[self.stock_index]]+list(map(lambda x:str(x["symbol"]+".PA"), list(stock_index)))
            try:
                stocks_ticker[stocks_ticker.index("MT.PA")]="MT.AS"
            except:
                pass
            stock_index = stock_data.get_stocks_by_index(self.stock_index)
            stocks_ticker2 = [self.stock_index_tickers[self.stock_index]]+list(map(lambda x:str(x["symbols"][0]["yahoo"]), list(stock_index)))
            for ticker in stocks_ticker :
                if ticker == stocks_ticker[0]:
                    self.data = pdr.get_data_yahoo(ticker, start=datetime.strptime(self.start_date, '%Y-%m-%d'), end=datetime.strptime(self.end_date, '%Y-%m-%d'))[["Close"]].fillna(method="bfill")
                    self.data.columns = [ticker]
                else:
                    try:
                        self.data[ticker] = pdr.get_data_yahoo(ticker, start=datetime.strptime(self.start_date, '%Y-%m-%d'), end=datetime.strptime(self.end_date, '%Y-%m-%d')).Close.fillna(method="bfill")
                    except:
                        i = stocks_ticker.index(ticker)
                        ticker = stocks_ticker2[i]
                        stocks_ticker[i] = ticker
                        self.data[ticker] = pdr.get_data_yahoo(ticker, start=datetime.strptime(self.start_date, '%Y-%m-%d'), end=datetime.strptime(self.end_date, '%Y-%m-%d')).Close.fillna(method="bfill")
            self.data.to_csv("data"+self.stock_index+".csv")
    def load_informations(self):
        pass        
    
    def run(self):
        self.load_data()
        n = 10
        price = np.array(self.data.iloc[:,0])
        #return_over_the_period = (price[1::4]-price[:len(price)-1:4])/price[:len(price)-1:4]
        #print(return_over_the_period)
        returns = pd.DataFrame((self.data.iloc[:,0]-self.data.iloc[:,0].shift(n))/self.data.iloc[:,0].shift(n))
        daily_returns = pd.DataFrame((self.data.iloc[:,0]-self.data.iloc[:,0].shift(1))/self.data.iloc[:,0].shift(1))
        for col in self.data.columns[1:]:
            returns[col] = (self.data[col]-self.data[col].shift(n))/self.data[col].shift(n)
            daily_returns[col] = (self.data[col]-self.data[col].shift(1))/self.data[col].shift(1)
        returns.fillna(0,inplace=True)
        daily_returns.fillna(0, inplace=True)
        returns.to_excel("returns_over_"+str(n)+"_periods"+self.stock_index+".xls")
        self.returns = returns
        self.daily_returns = daily_returns
        portfolio_value = 0
        self.summary = pd.DataFrame(np.array([0, 1000, None, None, None, None]).reshape(1,6), columns=["portfolio_value", "cash_account", "stock_held", "best_performer", "best_performance", "index_performance"], index = [returns.index[n]])
        for i in range(n,returns.shape[0]):
            best_performer = returns.columns[np.array(returns.iloc[i,1:]).argmax()+1]
            best_performance = np.array(returns.iloc[i,1:]).max()
            index_performance = returns.iloc[i,0]
            if i==n:
                portfolio_value = 1000
            else:
                portfolio_value = portfolio_value*(1+daily_returns[self.summary.iloc[i-n,3]].iloc[i,])
            self.summary.loc["Period "+str(i+1),:]=[portfolio_value, 0, best_performer, best_performer, best_performance, index_performance] 
        self.summary.set_index(returns.index[n-1:], inplace=True)
        