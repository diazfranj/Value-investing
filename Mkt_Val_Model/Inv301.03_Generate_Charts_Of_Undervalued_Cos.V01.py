# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 09:08:17 2016

@author: Russell
This prints out the charts of the current val inv ideas
"""

import numpy as np
import pandas as pd
import csv
from time import time
from os import chdir
import matplotlib.pyplot as plt

#chdir("/Users/Frank/Desktop/Mkt_Val_Model")
chdir("/Users/Frank/Desktop/Mkt_Val_Model/FInDat")
#read in the data
df = pd.read_csv("Inv201_05_All_Stock_Prices.csv",index_col="Date") #, index_col=False
splist = pd.read_csv("Inv301.03_ValInvStocks01.csv")
#Put in moving average
df200ma = pd.DataFrame.rolling(df.shift(1),window=200).mean()
  

#chdir("C:\\Russell\\Investment\\Python\\FinDat\\Charts")
chdir("C:\\Russell\\Investment\\Mkt_Val_Model\\FInDat\\Charts")
for i in range(0,len(splist)):    
    try:
      ticker = splist['Symbol'][i] 
      name = str(i) +'-' + ticker            
      ax = df[ticker].plot(title=name)
      ax = df200ma[ticker].plot()
      plt.show()
      #save thechart
      fig = ax.get_figure()
      fig.savefig('%r.png' % name, dpi=300)
      #del ax #doing this so that it doesnt put loads of charts on each other
      print str(i) + " of " + str(len(splist))
    except:
      pass

