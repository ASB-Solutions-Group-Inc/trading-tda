import os
import glob
# import pandas as pd
# from string import Template
# import numpy
import logging
# from setup import *
# Import to BQ
import subprocess


def query_example():
    cmd = (
        """bq load --autodetect --replace --source_format=CSV trading.trading_data output/ADBE.csv""")
    subprocess.call(cmd, shell=True)


def load_bq_portfolio(portfolio, log_message):
    cmd = (
        """bq load --autodetect --noreplace --source_format=CSV trading.trading_data output/""" +
        portfolio +
        '.csv')
    _output = subprocess.call(cmd, shell=True)
    log_message.info(
        str(portfolio) +
        " was loaded with the follwing " +
        str(_output))


def insert_first_portfolio(portfolio_ticker, log_message):
    cmd = (
        """bq load --autodetect --replace --source_format=CSV trading.trading_data output/""" +
        portfolio_ticker +
        ".csv")
    subprocess.call(cmd, shell=True)
    log_message.info("First portfolio loaded")


def load_bq():
    logging.basicConfig(
        filename='bqload.log'
        filemode='w',
        format='%(name)s - %(levelname)s - %(message)s'))
    os.chdir("output")
    for file in glob.glob("*.csv"):
        if file != "ADBE.csv":
            cmd = (
                """bq load --autodetect --noreplace --source_format=CSV trading.trading_data """ +
                file)
            output = subprocess.call(cmd, shell=True)
            logging.info(
                str(file) +
                "was loaded with the follwing" +
                str(output))

# query_example()
# load_bq()


# import pandas_ta as pta

# import pandas_datareader as pdr
# from datetime import datetime


# ticker = pdr.get_data_yahoo("MANH", datetime(2020, 1, 1))

# ticker['rsi'] = pta.rsi(ticker['Close'],timeperiod=13)
# print(ticker.tail())

# def importPortfolio():
#     df = pd.read_csv ('my-5-start-export.csv')
#     return df

# portfolio = importPortfolio()
# data = np.array(['ticker','open','high','low','close','volume','date'])
# dk = pd.DataFrame( columns=data)
# for row in range(len(portfolio)):
#     print(portfolio.loc[row,"Symbol"])


# print(API_KEY)
# df = pd.read_csv ('my-5-start-export.csv')
# print(df.head())
# data = np.array(['ticker','open','high','low','volume','date'])
# index = np.array(['ticker','date'])
# dk = pd.DataFrame(index =index, columns=data)

# print(dk)
