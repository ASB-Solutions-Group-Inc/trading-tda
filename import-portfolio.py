import pandas as pd
import csv
import numpy as np
from setup import *

# import pandas_datareader as pdr
# from datetime import datetime


# ticker = pdr.get_data_yahoo("TWTR", datetime(2020, 1, 1))
# print(ticker.head())
# print(ticker.shape)

def importPortfolio():
    df = pd.read_csv ('my-5-start-export.csv')
    return df

portfolio = importPortfolio()
data = np.array(['ticker','open','high','low','close','volume','date'])      
dk = pd.DataFrame( columns=data)
for row in range(len(portfolio)):
    print(portfolio.loc[row,"Symbol"])


# print(API_KEY)
# df = pd.read_csv ('my-5-start-export.csv')
# print(df.head())
# data = np.array(['ticker','open','high','low','volume','date'])                
# index = np.array(['ticker','date'])               
# dk = pd.DataFrame(index =index, columns=data)

# print(dk)