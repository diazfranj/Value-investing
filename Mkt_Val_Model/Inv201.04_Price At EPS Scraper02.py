# -*- coding: utf-8 -*-
"""
This downloads the price at each point in time of the eps
V.02 - So failed to downlaod the prices from yahoo, some wierd bug
- fixed by just using the new python.
Trying to add something to make the code time out after say 10 seconds
-------------------------
2018-01-24: need to put in an error report to show where price has not been brought back
2018-08-27: Change to make pandas_datareader work, line 21-23
2018-10/16: install data reader with "pip install pandas-datareader"
"""
import time
import pandas as pd
import pytz
from os import chdir
#from pandas.io.data import DataReader
#import pandas.io.data as web
from datetime import datetime
#fix for yahoo change
#https://stackoverflow.com/questions/50394873/import-pandas-datareader-gives-importerror-cannot-import-name-is-list-like
#fix for is lik error
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web ##NB! - PIP install this
#f = web.DataReader("F", 'yahoo', start, end)


#chdir("C:\\Python27\\tst")
chdir("C:\\Russell\\Investment\\Mkt_Val_Model")
epsdf = pd.read_csv("FinDat\\EpsSum01.csv",index_col=0) #, index_col=False

#mapping table for months
daysdf = pd.DataFrame([31,28,31,30,31,30,31,31,30,31,30,31], 
                      index=['01','02','03','04','05','06','07',
                      '08','09','10','11','12'],columns=['days'])

#pull out the list of all stocks in the index
StockList = list(epsdf.index)
#--------------------this pulls out the price for a day----------------
"""
This could be a function? what this is doing:
1.Pulls out a list of the current stock, with relevant headings
2.assigns the current date, starting with last day of month per mapping table
3. if len of data container is = 0 then it continues to try the previous day
4. it stops when it finds data, and stores it in the price[] list container.
5. it looks over the last five years to do this (there might be an error
on this if a stock has less than 5 years data)
"""
#create the big df to store all the data
AveTimeStart = time.time()
bigdf = pd.DataFrame(columns=['e1','e2','e3','e4','e5','p1','p2','p3','p4','p5'])
for z in range(1988,len(StockList)): #
  print "Number %r of %r" %(z,len(StockList))
  #just a particular line
  stName = StockList[z]
  CurStock = epsdf.loc[[stName]].dropna(axis=1,how='all')
  #start on -2
  #loop cycling through the last 5 years
  price = []#list to hold the prices
  start = time.time() #record the time for the process

  for j in range(0,5):  
    while (time.time() - start < 60):  #so give it 60 seconds to complete? 
        try: #try 1
          day = int(daysdf['days'][CurStock.columns[-(6-j):][0][5:]])
          #loop to try download the data give it 5 tries counting back
          data = [] #reset the data container
          for i in range(0,4):
                START = datetime(int(CurStock.columns[-(6-j):][0][:4])
                                ,int(CurStock.columns[-(6-j):][0][5:])
                                ,day
                                , 0, 0, 0, 0, pytz.utc) #year month day
                #Try download the data
                try:
                  data = web.DataReader(stName, 'yahoo', START, START)
                except:
                  pass
                day -= 1 #decrement the day
                if len(data) > 0: #if it brings back data exit the loop
                  break
            
          #store the data in a list
          try:    #try 2
            price.append(data['Close'][0])
          except: #try 2
            pass 
        except: #try 1
          pass
        if len(price) == j+1: #So this looks at the case where it returns nothing
            break
  #-----------------------------Status report---------------------------------
  AveTime = (time.time() - AveTimeStart) / (z+1)      
  print "%r time to harvest: %r Sec- Ave time: %r Sec- Time left: %r min/ %r hr " % (StockList[z],round(time.time() - start,2),
            round(AveTime,2), round(AveTime*(len(StockList)-z)/60,2),round(AveTime*(len(StockList)-z)/60/60,2))
  
  #save the EPS and price in new DF#################
  CurStock2 = CurStock.copy()
  ColLen = len(CurStock2.columns)
  epsList = [] #create a list to hold the EPS
  for i in range(0,5):
    try:
      epsList.append(CurStock2.loc[stName][ColLen-6+i])#so this picks a column by number
    except:
      epsList.append(0) #just incase there is not 5 years data?
  #combine the eps & price
  combList = epsList + price
  Analdf = pd.DataFrame(columns=['e1','e2','e3','e4','e5','p1','p2','p3','p4','p5'],
                        index=[stName])
  #populate the dataframe
  for i in range(0,len(combList)):
    Analdf[Analdf.columns[i]] = combList[i]
  #add the data to the big df
  bigdf = bigdf.append(Analdf)
  #---------------Save the file down----------------
  bigdf.to_csv("FinDat\\PriceEPSDat01.csv")
 
