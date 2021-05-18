# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 08:49:00 2018

@author: russe
"""

#functions used
from os import chdir
import pandas as pd
from datetime import datetime
import pytz
import time
#functions to download data
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web



#change directory and import the data
chdir("/Users/Frank/Desktop/Mkt_Val_Model")
epsdf = pd.read_csv("FinDat\\EpsSum01.csv", index_col=0)

#mapping table for months
daysdf = pd.DataFrame([31,28,31,30,31,30,31,31,30,31,30,31],
                      index=['01','02','03','04','05','06','07',
                             '08','09','10','11','12'],columns=['days'])

#pull out list of all stock in index
StockList = list(epsdf.index)

"""
1. Pull out a list of the current stock with relevant headings
2. Assign the current date, starting with the last day of the month per mapping table
3 if len of data container is = 0 then it continues to try the previous day
4.it stops when it finds data, and stores it in the price[] list container
5. it looks over the last five years to do this
"""

#create the big df to store all the data
AveTimeStart = time.time()
bigdf = pd.DataFrame(columns=['e1','e2','e3','e4','e5','p1','p2','p3','p4','p5'])
for z in range(0,len(StockList)): #len(StockList)
    print("Number {!r} of !{r}" % (z, len(StockList)))
    #just a particular line
    stName = StockList[z]
    CurStock = epsdf.loc[[stName]].dropna(axis=1,how='all')

    price = [] #list to hold the price data
    start = time.time()
    #read in data
    for j in range(0,5):
        try:
            day = int(daysdf['days'][CurStock.columns[-(6-j)][5:]])
            data = [] #reset the data container
            for i in range(0,4):
                START = datetime(int(CurStock.columns[-(6-j)][:4]),
                                 int(CurStock.columns[-(6-j)][5:]),
                                 day,
                                 0,0,0,0,pytz.utc)
                try:
                    data = web.DataReader(stName,'yahoo',START, START)
                except:
                    pass
                day -= 1
                if len(data) > 0: #if it brings back data exit loop
                    break
            
            #store the data in a list
            try:
                price.append(data['Close'][0])
            except:
                pass
        except:
            pass
        #if len(price) == j+1: #this looks at the case where it retuns nothing
        #    break
    #-----------------------Status report-------------------------
    AveTime = (time.time() - AveTimeStart) / (z+1)
    print("{!r} time to harvest: {!r} sec-Ave Time: {!r} sec- Time left: {!r} min/ {!r} hr" %(StockList[z]),
     round(time.time()-start,2),round(AveTime,2),round(AveTime*(len(StockList)-z)/60,2),round(AveTime*(len(StockList)-z)/60/60,2))
    #save the EPS and price in a new DF####################
    CurStock2 = CurStock.copy()
    ColLen = len(CurStock2.columns)
    epsList=[]
    for i in range(0,5):
        try:
            epsList.append(CurStock2.loc[stName][ColLen-6+i])
        except:
            epsList.append(0)
    "CombList = epsList + pricee3',"
    "Analdf = pd.DataFrame(columns=['e1','e2',''e4','e5','p1','p2','p3','p4','p5'],"
                              index= [stName]
    #populate the dataframe
    for i in range(0, len(CombList)):
        Analdf[Analdf.columns[i]] = CombList[i]
    #add the data to the big df
    bigdf = bigdf.append(Analdf)
    #-----------------save the file down-------------
    bigdf.to_csv("FinDat\\PriceEPSDat01.csv")













