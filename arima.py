

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import datetime
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf


# import sys
# debug=sys.argv[1]
# portfolio=sys.argv[2]
def converttodf (portfolio):
    df = pd.read_csv('output/' + portfolio + '.csv')
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)
    df.set_index('date', inplace=True)
    return df

def calculate_rsi(df,portfolio,debug):
    delta = df['close'].diff()
    up = delta.clip(lower=0)
    down = -1*delta.clip(upper=0)
    ema_up = up.ewm(com=13, adjust=False).mean()
    ema_down = down.ewm(com=13, adjust=False).mean()
    rs = ema_up/ema_down
    df['RSI'] = 100 - (100/(1 + rs))
    print(df.tail())
    return df

def calculate_arima (df, debug,portfolio) :
    # df = pd.read_csv('output/' + portfolio + '.csv')

    # df['date'] = pd.to_datetime(df['date'])
    # df.sort_values('date', inplace=True)
    # df.set_index('date', inplace=True)

    # if calculate_rsi_only == 'y':
    #     rs = calculate_rsi(df,portfolio,debug)
    #     print(rs.tail())
    #     return rs

    if debug == 'y':
        print(df.shape)
        print(df.head())

    df_week = df.resample('w').mean()
    df_week = df_week[['close']]
    if debug == 'y':
        print(df_week.head())

    df_week['weekly_ret'] = np.log(df_week['close']).diff()
    if debug == 'y':
        print(df_week.head())
    # drop null rows
    df_week.dropna(inplace=True)
    plt.figure(figsize=(12, 6))
    plt.title('weekly returns')
    plt.plot(df.close, label='weekly return')
    plt.savefig('output/plot/' + portfolio + '_return.png')
    #df_week.weekly_ret.plot(kind='line', figsize=(12, 6))
    udiff = df_week.drop(['close'], axis=1)

    if debug == 'y':
        print(udiff.tail())

    rolmean = udiff.rolling(20).mean()
    rolstd = udiff.rolling(20).std()
    if debug == 'y':
        print(rolmean.tail())
        print(rolstd.tail())
        plt.figure(figsize=(12, 6))
        orig = plt.plot(udiff, color='blue', label='Original')
        mean = plt.plot(rolmean, color='red', label='Rolling Mean')
        std = plt.plot(rolstd, color='black', label = 'Rolling Std Deviation')
        plt.title('Rolling Mean & Standard Deviation')
        plt.legend(loc='best')
        plt.show(block=False)
        plt.savefig('output/plot/' + portfolio + '.png')


    dftest = sm.tsa.adfuller(udiff.weekly_ret, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value ({0})'.format(key)] = value
        
    print(dfoutput)

    fig, ax = plt.subplots(figsize=(12,5))
    plot_acf(udiff.values, lags=20, ax=ax)
    plt.savefig('output/plot/' + portfolio + '_acf.png')

    fig, ax = plt.subplots(figsize=(12,5))
    plot_pacf(udiff.values, lags=20, ax=ax)
    plt.savefig('output/plot/' + portfolio + '_pacf.png')

    # Build ARIMA Model 
    from statsmodels.tsa.arima.model import ARIMA

    # Notice that you have to use udiff - the differenced data rather than the original data.
    ar1 = ARIMA(udiff.values, order = (3, 0,1)).fit()
    if debug == 'y':
        print(ar1.summary())


    steps = 5

    forecast = ar1.forecast(steps=steps)

    plt.figure(figsize=(12, 8))
    plt.plot(udiff.values, color='blue')

    preds = ar1.fittedvalues
    if debug == 'y':
        print(preds)
        print(forecast)
    plt.plot(preds, color='red')

    plt.plot(pd.DataFrame(np.array([preds[-1],forecast[0]]).T,index=range(len(udiff.values)+1, len(udiff.values)+3)), color='green')
    plt.plot(pd.DataFrame(forecast,index=range(len(udiff.values)+1, len(udiff.values)+1+steps)), color='green')
    plt.title('Display the predictions with the ARIMA model')
    plt.savefig('output/plot/' + portfolio + '_forcast.png')