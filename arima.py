import numpy as np
import pandas as pd
import pandas_ta as pta
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf
#from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import talib
# import datetime


# import sys
# debug=sys.argv[1]
# portfolio=sys.argv[2]
def convert_dataframe(portfolio):
    """This function will be used to convert the csv into the pandas dataframe"""
    data_portfolio = pd.read_csv('output/' + portfolio + '.csv')
    data_portfolio['date'] = pd.to_datetime(data_portfolio['date'])
    data_portfolio.sort_values('date', inplace=True)
    data_portfolio.set_index('date', inplace=True)
    return data_portfolio

def calculate_macd(ticker,logging):
    """This function will be used to calculate the MACD for the ticker symbol"""
    try:
        #macd_ = pta.macd(ticker['close'])
        macd = pta.macd(ticker['close'], fast=12, slow=26, signal=9)
        ticker = pd.concat([ticker,macd],axis=1)
    except Exception as error:
        logging.error("MACD error {0}".format(error))
    return ticker

def calculcate_cdl(ticker,logging):
    """This function will be used to calculate the cdl for the ticker symbol"""
    try: 
        df = ticker.ta.cdl_pattern(name="all")
        ticker = pd.concat([ticker,df],axis=1)
    except Exception as error:
        logging.error("CDL error {0} ".format(error))
        print("CDL error {0} ".format(error))
    return ticker

def calculate_rsi(ticker, logging):
    """This function will be used to calculate the RSI for the ticker symbol"""
    rsi = pta.rsi(ticker['close'], timeperiod=13)
    print(rsi.head())
    ticker = pd.concat([ticker,rsi],axis=1)
    ticker['Signal'] = 'KEEP'
    ticker.loc[ticker['RSI_14'] > 70, 'Signal'] = 'SELL'
    ticker.loc[ticker['RSI_14'] < 30, 'Signal'] = 'BUY'
    logging.info(ticker.tail())
    return ticker


def calculate_arima(data_portfolio, portfolio, logging):
    """This function will be used to calculate the ARIMA model"""
    # df = pd.read_csv('output/' + portfolio + '.csv')

    # df['date'] = pd.to_datetime(df['date'])
    # df.sort_values('date', inplace=True)
    # df.set_index('date', inplace=True)

    # if calculate_rsi_only == 'y':
    #     rs = calculate_rsi(df,portfolio,debug)
    #     logging.info(rs.tail())
    #     return rs
    if len(data_portfolio) == 0:
        return

    logging.info(data_portfolio.shape)
    logging.info(data_portfolio.head())

    df_week = data_portfolio.resample('w').mean()
    df_week = df_week[['close']]

    logging.info(df_week.head())

    df_week['weekly_ret'] = np.log(df_week['close']).diff()
    logging.info(df_week.head())
    # drop null rows
    df_week.dropna(inplace=True)
    plt.figure(figsize=(12, 6))
    plt.title('weekly returns')
    plt.plot(data_portfolio.close, label='weekly return')
    plt.savefig('output/plot/' + portfolio + '_return.png')
    udiff = df_week.drop(['close'], axis=1)

    logging.info(udiff.tail())

    rolmean = udiff.rolling(20).mean()
    rolstd = udiff.rolling(20).std()

    logging.info(rolmean.tail())
    logging.info(rolstd.tail())
    plt.figure(figsize=(12, 6))
    plt.plot(udiff, color='blue', label='Original')
    plt.plot(rolmean, color='red', label='Rolling Mean')
    plt.plot(rolstd, color='black', label='Rolling Std Deviation')
    plt.title('Rolling Mean & Standard Deviation')
    plt.legend(loc='best')
    plt.show(block=False)
    plt.savefig('output/plot/' + portfolio + '.png')

    dftest = sm.tsa.adfuller(udiff.weekly_ret, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4],
                         index=['Test Statistic',
                                'p-value',
                                '#Lags Used',
                                'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value ({0})'.format(key)] = value

    logging.info(dfoutput)

    fig, actuals = plt.subplots(figsize=(12, 5))
    plot_acf(udiff.values, lags=20, ax=actuals)
    plt.savefig('output/plot/' + portfolio + '_acf.png')

    fig, actuals = plt.subplots(figsize=(12, 5))
    plot_pacf(udiff.values, lags=20, ax=actuals)
    plt.savefig('output/plot/' + portfolio + '_pacf.png')

    # Build ARIMA Model
    # Notice that you have to use udiff - the differenced data rather than the
    # original data.
    ar1 = ARIMA(udiff.values, order=(3, 0, 1)).fit()
    logging.info(ar1.summary())
    with open('output/plot/' + portfolio + '_sarimax.txt', 'w') as file1:
        file1.writelines(str(ar1.summary()))
        file1.close()

    steps = 5

    forecast = ar1.forecast(steps=steps)

    plt.figure(figsize=(12, 8))
    plt.plot(udiff.values, color='blue')

    preds = ar1.fittedvalues

    logging.info(preds)
    logging.info(forecast)
    plt.plot(preds, color='red')

    plt.plot(pd.DataFrame(np.array([preds[-1],
                                    forecast[0]]).T,
                          index=range(len(udiff.values) + 1,
                                      len(udiff.values) + 3)),
             color='green')
    plt.plot(pd.DataFrame(forecast, index=range(len(udiff.values) +
             1, len(udiff.values) + 1 + steps)), color='green')
    plt.title('Display the predictions with the ARIMA model')
    plt.savefig('output/plot/' + portfolio + '_forcast.png')
