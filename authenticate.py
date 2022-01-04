import atexit
import datetime
import dateutil
from pandas.core.frame import DataFrame
import httpx
import sys
import tda
import pandas
import numpy
import json
# TD Ameritrade imports 
from tda.auth import easy_client
from tda.client import Client
from setup import *
from arima import * 


data = numpy.array(['ticker','open','high','low','close','volume','date'])
#index = numpy.array(['ticker','date'])               
dk = pandas.DataFrame( columns=data)

def importPortfolio():
    df = pandas.read_csv ('my-5-start-export.csv')
    return df

def make_webdriver():
    # Import selenium here because it's slow to import
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager

    driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver = webdriver.Chrome("/home/USER_NAME/FOLDER/chromedriver")
    # driver = webdriver.Chrome()
    # atexit.register(lambda: driver.quit())
    return driver

def getAccount(c, ACCOUNT_ID):
    account_information = c.get_account(ACCOUNT_ID,fields=Client.Account.Fields.POSITIONS)
    assert account_information.status_code == httpx.codes.OK
    account = pandas.DataFrame.from_dict(account_information.json())
    return account

c = tda.auth.easy_client(
    API_KEY,
    REDIRECT_URI,
    TOKEN_PATH,
    make_webdriver)

def getHistoricalData(dk, portfolio_ticker,reload,debug):
    print(portfolio_ticker)
    if (reload == 'y'):
        resp = c.get_price_history(portfolio_ticker,
            period_type=Client.PriceHistory.PeriodType.YEAR,
            period=Client.PriceHistory.Period.TWENTY_YEARS,
            frequency_type=Client.PriceHistory.FrequencyType.DAILY,
            frequency=Client.PriceHistory.Frequency.DAILY)
        assert resp.status_code == httpx.codes.OK
        data_hist = pandas.DataFrame.from_dict(resp.json())
        #print(data_hist['candles'][0])
        for i in data_hist['candles']:
            dk = dk.append({'ticker': portfolio_ticker,
                            'open': i['open'],
                            'high': i['high'],
                            'close' : i['close'],
                            'low': i['low'],
                            'volume': i['volume'],
                            'date': datetime.datetime.fromtimestamp(i['datetime']/1000) },ignore_index=True)
        dk = calculate_rsi(portfolio_ticker)
        # dk['date'] = pandas.to_datetime(dk['date'])
        # dk.sort_values('date', inplace=True)
        # dk.set_index('date', inplace=True)
        dk.to_csv("output/" + portfolio_ticker + ".csv",index=False)
    dt_portfolio = converttodf(portfolio_ticker)
    dt_portfolio = calculate_rsi(dt_portfolio,portfolio_ticker,'y')
    #calculate_arima(dt_portfolio,debug,portfolio=portfolio_ticker)
    return dk

#account_positions = tda.client.Client.Account.get_account()

account = getAccount(c, ACCOUNT_ID)
print(account)

portfolio = importPortfolio()
data = numpy.array(['ticker','open','high','low','close','volume','date'])      
dk = pandas.DataFrame( columns=data)
for row in range(len(portfolio)):
    getHistoricalData(dk, portfolio.loc[row,"Symbol"],RELOAD,DEBUG)

        
    






