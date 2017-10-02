# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 16:53:01 2015

@author: fantasie
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 14:23:52 2015

@author: fantasie
"""
""" Stock Prices Data Collector: Collect Historical Prices of Russel 1000 """
import csv
import datetime
import time
#import pandas as pd

from pandas.io.data import DataReader

begin = time.clock()
stocklist = csv.reader(file('Data/nasdaq.csv', 'rb'))

start_date = datetime.datetime(2010,1,5)
end_date = datetime.datetime(2014,12,31)

errorstock = []
stockuniv = []
for line in stocklist:
    symbol = line[0]
#    print symbol
    try:
        bars = DataReader(symbol, "yahoo", start_date, end_date)
        if '2010-01-05' in bars.index and '2014-12-31' in bars.index and len(bars) == 1257:
            bars.to_csv('Data/' + symbol+'.csv')
            stockuniv.append(symbol)
    except Exception as err:
        errorstock.append(symbol)
        print(err)
end = time.clock()
print "Time for data collecting: ", end - begin   
""" Store the list of stock universe """
writer = csv.writer(open('stockuniv.csv', 'wb'))
for item in stockuniv:
    writer.writerow([item])

""" Store the list of unavailable stocks"""
writer = csv.writer(open('errorstock.csv', 'wb'))
for item in errorstock:
    writer.writerow([item])
del writer
#print errorstock