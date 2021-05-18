# -*- coding: utf-8 -*-
"""
still to do, download the price at each interval for each stock
--------------------
So this just downloads the EPS
Prev Version:BeautSoupMStar Test08 SPList.py

>>>Morning star link<<<<:
You can find the link by going to the downloads page in chrome..copy link
By downloads I mean the list of all files downloaded in Chrome, it shows the source!!
Annual IS:
http://financials.morningstar.com/ajax/ReportProcess4CSV.html?&t=XNYS:STZ&region=usa&culture=en-US&cur=&reportType=is&period=12&dataType=A&order=asc&columnYear=5&curYearPart=1st5year&rounding=3&view=raw&r=519204&denominatorView=raw&number=3
Annual BS:
http://financials.morningstar.com/ajax/ReportProcess4CSV.html?&t=XNYS:STZ&region=usa&culture=en-US&cur=&reportType=bs&period=12&dataType=A&order=asc&columnYear=5&curYearPart=1st5year&rounding=3&view=raw&r=376739&denominatorView=raw&number=3
Annual CF:
http://financials.morningstar.com/ajax/ReportProcess4CSV.html?&t=XNYS:STZ&region=usa&culture=en-US&cur=&reportType=cf&period=12&dataType=A&order=asc&columnYear=5&curYearPart=1st5year&rounding=3&view=raw&r=243827&denominatorView=raw&number=3
Key Ratios:
http://financials.morningstar.com/finan/ajax/exportKR2CSV.html?&callback=?&t=XNAS:YHOO&region=usa&culture=en-US&cur=&order=asc
###Next
download all the cos as csv's and then create a big df per year,
headings along the top, cos down the side, and then I ave these
matrices to compare
#GO TO THE US VERSION OF THE SITE FOR THE DOWNOAD - put in stock, then select BS/CF/IE again to get the page
header, and then select "Key Ratios"..that gives you what to download
http://financials.morningstar.com/
if it brings back zero, try again?
--Dependant files---
"SPlist.csv"
--------------------
done to 65
if there is a dash in the name it replaces it with a dot..BRK-B =>BRK.B
02/17/2018: Updated read_csv to bring in data
"""

from bs4 import BeautifulSoup
import urllib2
import numpy as np
import pandas as pd
import csv
from os import chdir
from time import time
from time import sleep

#------------------function to open the webpage-----------------
def GetData(ticker,findf):
    #test to see if excahnge works "NYS" vs "NAS"-----------------------------
    istst = (r'http://financials.morningstar.com/ajax/ReportProcess4CSV.html?'+
              r'&t=XNYS:' + ticker + r'&region=usa&culture=en-US&cur=&reportType=is'+
              r'&period=12&dataType=A&order=asc&columnYear=5&curYearPart=1st5year&'+
              r'rounding=3&view=raw&r=519204&denominatorView=raw&number=3')
    header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
    req = urllib2.Request(istst,headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "lxml")
    if len(soup) == 0:
      ex = "NAS"
    else:
      ex = "NYS"
    #assign the tickers
    finwiki = (r'http://financials.morningstar.com/finan/ajax/exportKR2CSV.html?'+
              r'&callback=?&t=X'+ex+r':'+ticker+r'&region=usa&culture=en-US&cur=&order=asc')
    #links = [iswiki,bswiki,cfwiki,finwiki] #putting it all in a list
    links = [finwiki] #putting it all in a list
    #-----------------the rest of the code----------------
    header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
    req = urllib2.Request(links[0],headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "lxml")
    
    #------------------returned the I&E----------
    dat = soup.get_text() #pulls out just the text from the csv
    #just do a text thing
    #so create a file?
    target = open('test01.csv', 'w')
    target.write(dat)
    target.close()
    #can use skip rows?
    #---------------
    
    #read it in as a dataframe? skip the first row
    df = pd.read_csv("test01.csv",header = 2,index_col=False) #, index_col=False
    df.index = df['Unnamed: 0']
    df = df.drop(['Unnamed: 0'], axis = 1)
    df.index.names = ['Desc'] #rename the index
    #print(isdf)
    #to return the lines that I need
    dfeps = df.loc[['Earnings Per Share USD']].copy() #,'Return on Assets %'
    #so the technique to change the name is to add a column
    dfeps['name'] = ticker
    dfeps.index =  dfeps['name']    
    del dfeps['name']
    #change the name of the colums to last years, to make it consistant?
    #then can do valuation in excel...no need to pull in price at each period
    ################now combine the two df's###############
    if j==0:  
      findf = dfeps
    else:  
      findf = findf.append(dfeps) #the merged BS/IS
    return findf

    
#start time
t1 = time()
#read in the S&P500
#chdir("C:\\Python27\\tst")
chdir("C:\\Russell\\Investment\\Mkt_Val_Model")
splist = pd.read_csv("Inv201.02_List_All_US_Stocks_500m_INPY.csv",index_col=None) #, index_col=False
##NYS of NAS...a flag to say if its Nasdaq or NYSE
#so put in a test to see if the link brings back anything, and then
#set the flag to either nasdaq or NYSE
#create the DF
findf = pd.DataFrame()
FailedAttempt = [] #store the names of stocks that have failed
#loop
for j in range(0,len(splist)):#len(splist)
  #initialise the attempt tracker
  Attempt = 0
  ticker = splist['Symbol'][j].replace("-",".") #the start"STZ" , apple is nasdaq..
  #status------------------------------------------------------------------
  AveTime = round((time() - t1)/(j+1))
  print "Number {!r} of {!r}: {!s} Ave time: {!r} sec Time left: {!r} min/{!r} hrs".Format %(j,len(splist),
          ticker,AveTime,round(AveTime * (len(splist)-j)/60,2),round(AveTime * (len(splist)-j)/60/60,2))  
  for k in range(0,10): #try 10 times  
      try:
          findf = GetData(ticker,findf)  
          Attempt += 1 #increment the report of number fo tries
          break #this exits the loop because it worked
      except:
          sleep(3) #wait 3 seconds until the next attempt
          Attempt += 1 #increment the report of number fo tries
          if Attempt == 10:
              FailedAttempt.append(ticker)
            
  #save it each time, just so if it crashes I can pick up from where it crashed
  findf.to_csv("FinDat\\EpsSum01.csv")
  #save the failed attempt to a series in pandas, then save to csv
  FailedSeries = pd.Series(FailedAttempt)
  FailedSeries.to_csv("FinDat\\FailedTicker01.csv")
  print j, Attempt
    
#print time() - t1

#------------------------save it all down------------------
findf.to_csv("FinDat\\EpsSum01.csv")
#------------------------------
#NB: How to bring back just the relevant columns
#findf.loc[['A']].dropna(axis=1,how='all')