# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 08:29:21 2018

@author: russell
This code scrapes the market cap value from the Zacks website, for a given list of stocks.
"""
#Funtions being used
from os import chdir
import numpy as np
import pandas as pd
from time import time
#functions for webscraping
from bs4 import BeautifulSoup
import urllib2

#Change to the right folder & read in data to a dataframe
chdir("C:\\Russell\\Investment\\Mkt_Val_Model")
colist = pd.read_csv("Inv201.02_List_All_US_Stocks_INPY.csv",index_col=None)

#create an empty list to store all the market caps, then populate with zeros
#populated with zeros initially so that file can be saved as it downloads data
mcaplist = []
for i in range(0,len(colist)):
    mcaplist.append(0)

#Collect Market caps
StartTime = time() #record the absolute start time before the loop runs
for i in range(0,len(colist)):
    t1 = time() #record the start time
    #-------------------------------Scrape the data from the website & save to mcaplist---------------------
    try:
        header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error
        req = urllib2.Request("http://www.zacks.com/stock/quote/" + colist['Symbol'][i],headers=header)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page, "lxml")
        for tr in soup.findAll("table", class_="abut_bottom"):
            for td in tr.find_all("td"):
                if td.text == "Market Cap":
                    #print td.text, td.find_next_sibling("td").text
                    mcaplist[i] = td.find_next_sibling("td").text
    except:
        mcaplist[i] = 0 #kind of redundant because zero is already there.
    #-------------------------------status report while running---------------------------------------------
    t2 = time() - t1 #record the end time
    #total time elapsed / number of stocks evaluated, +1 because python starts at 0
   AveTime = (time() - StTime) / (i + 1)
  print("{!r} of {!r}- Ave time: {!r} sec- Time left: {!r} min/ {!r} hr".format(i, len(splist), round(AveTime, 2), round(AveTime * (len(splist)-i)/60,2), round(AveTime * (len(splist)-i)/60/60,2)))  
    #-------------------------------save in case of crash---------------------------------------------------
    #put the list in the dataframe  
    colist['mcap'] = mcaplist
    #save it to a file
    colist.to_csv("Inv201.02_List_All_US_Stocks_wMCap_OUTPY.csv")