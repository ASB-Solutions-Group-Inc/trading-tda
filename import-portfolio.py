import pandas as pd
import csv
import numpy as np
from setup import *

print(API_KEY)
df = pd.read_csv ('my-5-start-export.csv')
print(df.head())
data = np.array(['ticker','open','high','low','volume','date'])                
index = np.array(['ticker','date'])               
dk = pd.DataFrame(index =index, columns=data)

print(dk)