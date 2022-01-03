#%matplotlib inline

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

import sys
debug=sys.argv[1]
portfolio=sys.argv[2]

#%config InlineBackend.figure_format = 'retina'
df = pd.read_csv('output/' + portfolio + '.csv')

df['date'] = pd.to_datetime(df['date'])
df.sort_values('date', inplace=True)
df.set_index('date', inplace=True)

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
df_week.weekly_ret.plot(kind='line', figsize=(12, 6))
udiff = df_week.drop(['close'], axis=1)

if debug == 'y':
    print(udiff.tail())

rolmean = udiff.rolling(20).mean()
rolstd = udiff.rolling(20).std()
if debug == 'y':
    print(rolmean.tail())
    print(rolstd.tail())