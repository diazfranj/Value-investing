# -*- coding: utf-8 -*-
"""
so this downloads just the close of each of the S&P 500, for say the last 
5 years - i can create a 500 column matrix? of whatever the information I need
..so definately close, volume?..just close and date for now,
im looking for a trend.
..remember NASDAQ..this is just S&P500
V.05: Updated for change in python, changed to pd.read_csv to read in list
# potentially need to "disable some files"
https://github.com/ContinuumIO/anaconda-issues/issues/8561

"""

import pandas as pd
import numpy as np
import pytz
from os import chdir
#from pandas.io.data import DataReader
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web #New
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from time import time

#chdir("C:\\Russell\\Investment\\Python")
chdir("/Users/Frank/Desktop/Mkt_Val_Model")

#Bn dollar stocks
splist = pd.read_csv("Inv201.02_List_All_US_Stocks_500m_INPY.csv",index_col=None) #, index_col=False
#Just the S&P 500
#splist = pd.DataFrame.from_csv(path = "SPlist3SP500.csv", index_col=False)

#NNB!- this data is used to chart all the stocks so I can pick, so more data is better
#START = datetime(2016, 5, 21, 0, 0, 0, 0, pytz.utc) #Year/Month/Day
END = datetime.today().utcnow()
START = END - timedelta(365*2) #2 years ago from today

data = web.DataReader('GOOG', 'yahoo', START, END) #splist['name'][0]

#sve the data to a bigger df - the first one
sp500 = data[['Close']]
#removes the column name, can then loop and populate close data
del sp500['Close'] 

StTime = time()
for i in range(0,len(splist)):
  try:    
    data = web.DataReader(splist['Symbol'][i], 'yahoo', START, END)
    #populate the big list
    sp500[splist['Symbol'][i]] = data['Close'].copy()
  except:
    pass
  sp500.to_csv('Inv301.02_Dcf_valuation_of_stocks.V02.csv')
  #-------------------Status report---------------------
  AveTime = (time() - StTime) / (i + 1)
  print("{!r} of {!r}- Ave time: {!r} sec- Time left: {!r} min/ {!r} hr".format(i, len(splist), round(AveTime, 2), round(AveTime * (len(splist)-i)/60,2), round(AveTime * (len(splist)-i)/60/60,2)))