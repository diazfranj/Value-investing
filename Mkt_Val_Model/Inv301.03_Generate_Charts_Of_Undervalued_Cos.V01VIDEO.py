# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 09:43:19 2018

@author: russe
This prints out the charts of the current val investment ideas
"""

#functions
from os import chdir
import pandas as pd
import matplotlib.pyplot as plt

#change directory
chdir("C:\\Russell\\Investment\\Mkt_Val_Model\\FInDat")
#read in the data
df = pd.read_csv("Inv201_05_All_Stock_Prices.csv", index_col="Date")
splist = pd.read_csv("Inv301.03_ValInvStocks01.csv")

#put in moving average
df200ma = pd.DataFrame.rolling(df,window=200).mean()

#change directory to save charts
chdir("C:\Russell\Investment\Mkt_Val_Model\FInDat\Charts")
for i in range(0,len(splist)):
    try:
        ticker = splist['Symbol'][i]
        name = str(i) + '-' + ticker
        ax = df[ticker].plot(title=name)
        ax = df200ma[ticker].plot()
        plt.show()
        #save the chart
        fig = ax.get_figure()
        fig.savefig('%r.png' % name, dpi=300)
        print str(i) + " of " + str(len(splist))
    except:
        pass
