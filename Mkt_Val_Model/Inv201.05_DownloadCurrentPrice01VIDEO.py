# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 09:25:38 2018

@author: russe
"""

#functions used------------------
from os import chdir
import pandas as pd
from datetime import datetime, timedelta
from time import time
#webscraping functions
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web

#changing directory---------------
chdir("C:\\Russell\\Investment\\Mkt_Val_Model")
splist = pd.read_csv("Inv201.02_List_All_US_Stocks_500m_INPY.csv", index_col=None)

#-----read in data---------------
END = datetime.today().utcnow()
START = END - timedelta(365*2)

data = web.DataReader('GOOG', 'yahoo', START, END)

#---------data containter-----------------
sp500 = data[['Close']]
#delete close
del sp500['Close']

StTime = time()
#-------------------the loop------------------
for i in range(0,len(splist)): #len(splist)
    try:
        data = web.DataReader(splist['Symbol'][i], 'yahoo', START, END)    
        # put into data container
        sp500[splist['Symbol'][i]] = data['Close'].copy()
    except:
        pass
    sp500.to_csv("FinDat\\Inv201_05_All_Stock_Prices.csv")
    #----------------------Status report-------------------------
    AveTime = (time()- StTime) / (i + 1)
    print "%r of %r- Ave time: %r sec- Time left: %r min/ %r hr" %(i,len(splist),
        round(AveTime,2), round(AveTime * (len(splist)-i)/60,2),round(AveTime * (len(splist)-i)/60/60,2))
    
    
    