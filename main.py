# pylint: disable=redefined-outer-name
# import sys
# import atexit
import datetime
import logging
# import dateutil
# from pandas.core.frame import DataFrame
import httpx
import tda
import pandas
import numpy
# TD Ameritrade imports
#from tda.auth import easy_client
from tda.client import Client
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from setup import *
from arima import calculate_rsi,convert_dataframe,calculate_arima
from load_bq import insert_first_portfolio,load_bq_portfolio


def import_portfolio(logging):
    """This function will be used to import the portfolio """
    data_csv = pandas.read_csv('my-5-start-export.csv')
    logging.info("Portfolio CSV file loaded")
    return data_csv


def make_webdriver():
    """Import selenium here because it's slow to import"""
    driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver = webdriver.Chrome("/home/USER_NAME/FOLDER/chromedriver")
    # driver = webdriver.Chrome()
    # atexit.register(lambda: driver.quit())
    return driver


def get_account(client, account_id, logging):
    """This function will be used to get the accounts """
    account_information = client.get_account(
        account_id, fields=Client.Account.Fields.POSITIONS)
    if account_information.status_code != httpx.codes.OK:
        logging.error(str(account_information.status_code))
    account = pandas.DataFrame.from_dict(account_information.json())
    return account


_client = tda.auth.easy_client(
    API_KEY,
    REDIRECT_URI,
    TOKEN_PATH,
    make_webdriver)


def get_historical_data(data_portfolio, portfolio_ticker, reload, logging):
    """This function will be used to get historical data of the portfolio ticker """
    logging.info('portfolio started loading' + portfolio_ticker)
    if reload == 'y':
        resp = _client.get_price_history(
            portfolio_ticker,
            period_type=Client.PriceHistory.PeriodType.YEAR,
            period=Client.PriceHistory.Period.TWENTY_YEARS,
            frequency_type=Client.PriceHistory.FrequencyType.DAILY,
            frequency=Client.PriceHistory.Frequency.DAILY)
        assert resp.status_code == httpx.codes.OK
        data_hist = pandas.DataFrame.from_dict(resp.json())
        for i in data_hist['candles']:
            data_portfolio = data_portfolio.append({'ticker': portfolio_ticker,
                            'open': i['open'],
                            'high': i['high'],
                            'close': i['close'],
                            'low': i['low'],
                            'volume': i['volume'],
                            'date': datetime.datetime.fromtimestamp(i['datetime'] / 1000)},
                           ignore_index=True)
        data_portfolio = calculate_rsi(data_portfolio, logging)
        data_portfolio.to_csv("output/" + portfolio_ticker + ".csv", index=False)

#account_positions = tda.client.Client.Account.get_account()
def real_time_quote(client,portfolio):
    """This function will be used to get the real time quotes """
    _response = client.get_quote(portfolio)
    print(_response.json())
    return _response

def read_spark_csv(filename):
    spark_dataframe = pandas.read_csv(filename)
    return spark_dataframe

def main():
    """This is the main function """
    if DEBUG == 'y':
        logging.basicConfig(
            filename='app.log',
            filemode='w',
            level=logging.DEBUG,
            format='%(name)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(
            filename='app.log',
            filemode='w',
            format='%(name)s - %(levelname)s - %(message)s')
    # account = get_account(c, ACCOUNT_ID,logging)
    portfolio = import_portfolio(logging)
    #spark_portfolio = read_spark_csv("SPARK.csv")
    #load_spark_portfolio(spark_portfolio)
    data = numpy.array(
        ['ticker', 'open', 'high', 'low', 'close', 'volume', 'date'])
    _dk = pandas.DataFrame(columns=data)
    count = 0
    for row in range(len(portfolio)):
        portfolio_ticker = portfolio.loc[row, "Symbol"]
        get_historical_data(_dk, portfolio_ticker, RELOAD, logging)
        if RUN_AMIRA == 'y':
            try:
                dt_portfolio = convert_dataframe(portfolio_ticker)
                calculate_arima(dt_portfolio, portfolio_ticker, logging)
            except Exception as error:
                logging.error(error)
        if RELOAD == 'y':
            load_bq_portfolio(portfolio_ticker, logging, count)
            count = count + 1
if __name__ == '__main__':
    main()
