# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 08:35:30 2018

@author: russe
Reads in data from the http://financials.morningstar.com/ website, and extracts the EPS
data for a given list of stocks.
"""

#functions used
from os import chdir
import pandas as pd
import csv
from time import time
from time import sleep
#webscraping functions
from bs4 import BeautifulSoup
import urllib2


#---------------------function to collect data--------------
def GetData(ticker,findf):
    #-----------------------Reading in data from Morningstar website------------------------
    #Apple Web Address
    #http://financials.morningstar.com/finan/ajax/exportKR2CSV.html?&callback=?&t=XNAS:AAPL&region=usa&culture=en-US&cur=&order=asc
    
    #Testing which exchange the stock is on
    istst = (r'http://financials.morningstar.com/finan/ajax/exportKR2CSV.html?&callback=?&t=XNYS:'
             + ticker + 
             r'L&region=usa&culture=en-US&cur=&order=asc')
    header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error 
    req = urllib2.Request(istst, headers = header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "lxml")
    if len(soup) == 0:
        ex = "NAS"
    else:
        ex = "NYS"
    # Assign the tickers
    finwiki = (r'http://financials.morningstar.com/finan/ajax/exportKR2CSV.html?&callback=?&t=X' +
               ex + r':'
             + ticker + 
             r'L&region=usa&culture=en-US&cur=&order=asc')
    #-------------------------Pull out data from the website--------
    header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error 
    req = urllib2.Request(finwiki, headers = header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "lxml") 
    #-------return earnings per share data-----------
    dat = soup.get_text()
    target = open('test01.csv', 'w')
    target.write(dat)
    target.close()
    #--------read into a dataframe-----------------
    df = pd.read_csv('test01.csv', header = 2, index_col=False)
    df.index = df['Unnamed: 0']
    df = df.drop(['Unnamed: 0'], axis = 1)
    df.index.names = ['Desc']
    #----pull out the EPS data
    dfeps = df.loc[['Earnings Per Share USD']].copy()
    dfeps['name'] = ticker
    dfeps.index = dfeps['name']
    del dfeps['name']
    ###############combine the two dataframes######################
    if j ==0:
        findf = dfeps #for the first time
    else:
        findf = findf.append(dfeps) #else just append   
    return findf    

#import data
chdir("C:\\Russell\\Investment\\Mkt_Val_Model")
splist = pd.read_csv("Inv201.02_List_All_US_Stocks_500m_INPY.csv", index_col=None)
#Main dataframe to store data
findf = pd.DataFrame()
FailedAttempt = [] #store the names of stocks that have failed
t1 = time()
for j in range(0,len(splist)): #len(splist)
    Attempt = 0
    #Read in stock name (ticker)-------------
    ticker = splist['Symbol'][j].replace("-",".")
    #---------------------Status report-----------------
    AveTime = round((time() - t1) / (j+1),2)
    print "Number %r of %r: %r Ave time: %r sec Time left: %r min/%r hrs" %(j,len(splist),
        ticker, AveTime, round(AveTime * (len(splist)-j)/60,2),round(AveTime * (len(splist)-j)/60/60,2))
    
    for k in range(0,10): #try 10 times
        try:
            findf = GetData(ticker, findf)
            Attempt += 1
            break #exits loop
        except:
            sleep(3)
            Attempt += 1
            if Attempt == 10:
                FailedAttempt.append(ticker)
    #Saving data to file
    findf.to_csv("FinDat\\EpsSum01.csv")
    FailedSeries = pd.Series(FailedAttempt)            
    FailedSeries.to_csv("FinDat\\FailedTicker01.csv")
                
    print j, Attempt
   
    
    








       
        
        
        
        
    