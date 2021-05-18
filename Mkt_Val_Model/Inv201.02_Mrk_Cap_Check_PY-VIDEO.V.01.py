# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 07:28:13 2018

@author: russe
This code scrapes the market cap value from the Zacks website, for a give list of stocks.
"""

#functions being used
from os import chdir
import pandas as pd
from time import time
#funtions for webscraping
from bs4 import BeautifulSoup
import urllib2


#change to the right folder & read in data to a dataframe
chdir("/Users/Frank/Desktop/Mkt_Val_Model")
colist = pd.read_csv("Inv201.02_List_All_US_Stocks_INPY.csv",index_col=None)

#create an empty list to store all the market caps
mcaplist = []
for i in range(0,len(colist)):
    mcaplist.append(0)

StartTime = time()
#Collect Market Cap data
for i in range(0,len(colist)): #len(colist)
    t1 = time() #record start time
    #-------------------------------------scrape the data from the website & save to mcaplist---------
    try:
        header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error
        req = urllib2.Request("https://www.zacks.com/stock/quote/" + colist['Symbol'][i],headers=header)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page, "lxml")
        for tr in soup.findAll("table",class_="abut_bottom"):
            for td in tr.find_all("td"):
                if td.text == "Market Cap":
                    #print td.text, td.find_next_sibling("td").text
                    #mcaplist.append(td.find_next_sibling("td").text)
                    mcaplist[i] = td.find_next_sibling("td").text
    except:
        mcaplist[i] = 0 #kind of redundant
    #-----------------------------------status report while running-------------------
    AveTime = (time() - StTime) / (i + 1)
  print("{!r} of {!r}- Ave time: {!r} sec- Time left: {!r} min/ {!r} hr".format(i, len(splist), round(AveTime, 2), round(AveTime * (len(splist)-i)/60,2), round(AveTime * (len(splist)-i)/60/60,2)))
    #-----------------------------------save in case of crash----------------------
    #put list in the dataframe
    colist['mcap'] = mcaplist     
    #save it to a file
    colist.to_csv("Inv201.02_List_All_US_Stocks_wMCap_OUTPY.csv")    



    
    
    
    
    
    
    
    
