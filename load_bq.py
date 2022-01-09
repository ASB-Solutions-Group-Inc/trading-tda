import os
import glob
# import pandas as pd
# from string import Template
# import numpy
import logging
# from setup import *
# Import to BQ
import subprocess


def query_example(portfolio):
    """This function will be used to load one portfolio file with table recreate"""
    cmd = (
        """bq load --autodetect --replace --source_format=CSV trading.trading_data""" 
        + "output/"
        + portfolio
        + ".csv")
    subprocess.call(cmd, shell=True)


def load_bq_portfolio(portfolio, log_message,count):
    """This function will be used to load data into BQ for a given portfolio"""
    if count == 0:
        cmd = (
            """bq load --autodetect --replace --source_format=CSV trading.trading_data output/""" +
            portfolio +
            ".csv")
    else:
        cmd = (
            """bq load --autodetect --noreplace --source_format=CSV trading.trading_data output/""" +
            portfolio +
            '.csv')
    _output = subprocess.call(cmd, shell=True)
    log_message.info(
        str(portfolio) +
        " was loaded with the follwing " +
        str(_output))

def load_spark_portfolio():
    """This function will load the spark dataframe to BQ"""
    cmd = (
        """bq load --autodetect --replace --source_format=CSV trading.spark_portfolio SPARK.csv"""
    )
    subprocess.call(cmd, shell=True)
    logging.info("spark portfolio loaded")

def load_bq(exclude_file):
    """This function will be used to load all the files in the folder into BQ except the filename that is passed """
    logging.basicConfig(
        filename='bqload.log',
        filemode='w',
        format='%(name)s - %(levelname)s - %(message)s')
    os.chdir("output")
    for file in glob.glob("*.csv"):
        if file != exclude_file :
            cmd = (
                """bq load --autodetect --noreplace --source_format=CSV trading.trading_data """ +
                file)
            output = subprocess.call(cmd, shell=True)
            logging.info(
                str(file) +
                "was loaded with the follwing" +
                str(output))

# Reload the data from this script, the first portfolio that will be loaded is ADBE
# query_example("ADBE")
# load_bq("ADBE.csv")


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
