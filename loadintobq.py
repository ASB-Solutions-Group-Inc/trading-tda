import pandas as pd
import csv
import numpy as np
from setup import *

## Import to BQ 
import subprocess

def query_example(): 
    cmd =("""bq load --autodetect --replace --source_format=CSV trading.trading_data output/ADBE.csv""")
    subprocess.call(cmd,shell=True)


import glob, os

def loadintobq():
    os.chdir("output")
    for file in glob.glob("*.csv"):
        if file != "ADBE.csv":
            cmd =("""bq load --autodetect --noreplace --source_format=CSV trading.trading_data """ + file)
            y = subprocess.call(cmd,shell=True)
            print (file + "was loaded with the follwing" + y)











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