

import pandas_ta as pta
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
# import datetime


# import sys
# debug=sys.argv[1]
# portfolio=sys.argv[2]
def converttodf(portfolio):
    df = pd.read_csv('output/' + portfolio + '.csv')
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)
    df.set_index('date', inplace=True)
    return df


def calculate_rsi(ticker, logging):
    ticker['rsi'] = pta.rsi(ticker['close'], timeperiod=13)
    ticker['Signal'] = 'KEEP'
    ticker.loc[ticker['rsi'] > 70, 'Signal'] = 'SELL'
    ticker.loc[ticker['rsi'] < 30, 'Signal'] = 'BUY'
    logging.info(ticker.tail())
    return ticker


def calculate_arima(df, portfolio, logging):
    # df = pd.read_csv('output/' + portfolio + '.csv')

    # df['date'] = pd.to_datetime(df['date'])
    # df.sort_values('date', inplace=True)
    # df.set_index('date', inplace=True)

    # if calculate_rsi_only == 'y':
    #     rs = calculate_rsi(df,portfolio,debug)
    #     logging.info(rs.tail())
    #     return rs
    if len(df) == 0:
        return

    logging.info(df.shape)
    logging.info(df.head())

    df_week = df.resample('w').mean()
    df_week = df_week[['close']]

    logging.info(df_week.head())

    df_week['weekly_ret'] = np.log(df_week['close']).diff()
    logging.info(df_week.head())
    # drop null rows
    df_week.dropna(inplace=True)
    plt.figure(figsize=(12, 6))
    plt.title('weekly returns')
    plt.plot(df.close, label='weekly return')
    plt.savefig('output/plot/' + portfolio + '_return.png')
    #df_week.weekly_ret.plot(kind='line', figsize=(12, 6))
    udiff = df_week.drop(['close'], axis=1)

    logging.info(udiff.tail())

    rolmean = udiff.rolling(20).mean()
    rolstd = udiff.rolling(20).std()

    logging.info(rolmean.tail())
    logging.info(rolstd.tail())
    plt.figure(figsize=(12, 6))
    orig = plt.plot(udiff, color='blue', label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label='Rolling Std Deviation')
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

    fig, ax = plt.subplots(figsize=(12, 5))
    plot_acf(udiff.values, lags=20, ax=ax)
    plt.savefig('output/plot/' + portfolio + '_acf.png')

    fig, ax = plt.subplots(figsize=(12, 5))
    plot_pacf(udiff.values, lags=20, ax=ax)
    plt.savefig('output/plot/' + portfolio + '_pacf.png')

    # Build ARIMA Model
    from statsmodels.tsa.arima.model import ARIMA

    # Notice that you have to use udiff - the differenced data rather than the
    # original data.
    ar1 = ARIMA(udiff.values, order=(3, 0, 1)).fit()
    logging.info(ar1.summary())
    file1 = open('output/plot/' + portfolio + '_sarimax.txt', "w")
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
