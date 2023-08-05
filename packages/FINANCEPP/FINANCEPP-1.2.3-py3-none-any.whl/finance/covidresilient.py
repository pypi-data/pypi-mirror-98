import pandas as pd
import numpy as np
from datetime import datetime
import pandas_datareader as pdr


class CovidResilience:
    def __init__(self, stock_index = "STOXX 600", start_date = None, end_date = None, tickers = None):
        self.stock_index = stock_index
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.informations = None
        self.stock_index_tickers = {"CAC 40":"^FCHI","BEL 20":"^BFX", "S&P 500":"^GSPC", "STOXX 600":"^STOXX"}
        self.returns = None #on the period
        self.daily_returns = None #daily
        self.path_to_data = None
        self.stocks_selection = "covid_resilient"
        self.relevant_data = None
        self.relevant_data_returns = None
        self.volatilities = None
        self.rslt = None
        if tickers != None:
            self.tickers = tickers

    def load_data(self):
        if self.path_to_data:
            self.data = pd.read_csv(self.path_to_data, parse_dates = True, index_col=0)
        else:
            stocks_ticker = [self.stock_index_tickers[self.stock_index]] + self.tickers
            for ticker in stocks_ticker :
                if ticker == stocks_ticker[0]:
                    self.data = pdr.get_data_yahoo(ticker, start=datetime.strptime(self.start_date, '%Y-%m-%d'), end=datetime.strptime(self.end_date, '%Y-%m-%d'))[["Close"]].fillna(method="bfill")
                    self.data.columns = [ticker]
                else:
                    try:
                        try:
                            self.data[ticker] = pdr.get_data_yahoo(ticker, start=datetime.strptime(self.start_date, '%Y-%m-%d'), end=datetime.strptime(self.end_date, '%Y-%m-%d')).Close.fillna(method="bfill")
                        except:
                            self.data[ticker] = pdr.get_data_yahoo(ticker.replace("-A","A"), start=datetime.strptime(self.start_date, '%Y-%m-%d'), end=datetime.strptime(self.end_date, '%Y-%m-%d')).Close.fillna(method="bfill")
                    except:
                        print("Not in "+ticker)
          #self.data.to_csv("data.csv")

    def stocks_selector(self):
      if self.stocks_selection == "covid_resilient":
          relevant_dates = ["2020-01-20", "2020-03-18","2020-10-28","2021-01-19"]
          self.relevant_data = self.data.loc[relevant_dates, :]

    def compute_returns(self):
        # Compute daily returns on the whole period and at the same time
        self.daily_returns = pd.DataFrame((self.data.iloc[:,0]-self.data.iloc[:,0].shift(1))/self.data.iloc[:,0].shift(1))
        for col in self.data.columns[1:]:
            self.daily_returns[col] = (self.data[col]-self.data[col].shift(1))/self.data[col].shift(1)
        self.daily_returns.fillna(0, inplace=True)
        #daily_returns.to_excel("daily_returns"+self.stock_index+".xls")
        #self.daily_returns.to_csv("returns.csv")
        # Compute returns of relevant data in case we use the covid_resilient selector
        if self.stocks_selection == "covid_resilient":
            self.relevant_data_returns = pd.DataFrame((self.relevant_data.iloc[:,0]-self.relevant_data.iloc[:,0].shift(1))/self.relevant_data.iloc[:,0].shift(1))
            for col in self.relevant_data.columns[1:]:
                self.relevant_data_returns[col] = (self.relevant_data[col]-self.relevant_data[col].shift(1))/self.relevant_data[col].shift(1)
            self.relevant_data_returns.fillna(0, inplace=True)
    
    def compute_volatilities(self):
        self.volatilities = pd.DataFrame(self.daily_returns.std(axis=0, skipna =True), columns=["vol_over_the_period"]) # annualiser
        if self.stocks_selection == "covid_resilient":
            for i in range(len(self.relevant_data.index)-1):
                dt1 = self.relevant_data.index[i]
                dt2 = self.relevant_data.index[i+1]
                self.volatilities["vol_"+str(dt1)+"_"+str(dt2)] = self.daily_returns.loc[dt1:dt2, :].std(axis = 0, skipna =True) # a annualise
    def run(self):
        self.load_data()
        self.stocks_selector()
        self.compute_returns()
        self.compute_volatilities()

        a=self.relevant_data_returns.quantile(q=0.25, axis=1)[1]
        rslt = pd.DataFrame(self.relevant_data_returns.loc[["2020-03-18"],:]>a)
        b=self.relevant_data_returns.quantile(q=0.25, axis=1)[2]
        rslt = pd.concat([rslt,self.relevant_data_returns.loc[["2020-10-28"],:]>b])
        c=self.relevant_data_returns.quantile(q=0.25, axis=1)[3]
        rslt = pd.concat([rslt,self.relevant_data_returns.loc[["2021-01-19"],:]>c])

        for i in range(4):
            d = self.volatilities.T.quantile(q=0.25, axis=1)[i]
            rslt = pd.concat([rslt,self.volatilities.T.loc[[self.volatilities.columns[i]],:]<d])
        self.rslt = rslt.astype(int)
        self.rslt.loc["criterion", :] = self.rslt.sum(axis=0)
        self.rslt.sort_values(by="criterion", axis=1, ascending = False)
      