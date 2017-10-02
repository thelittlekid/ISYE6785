# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 10:08:12 2015

@author: fantasie
"""

import csv
import pandas as pd
import numpy as np
import time
from math import sqrt

#%% Global variables are defined below
shifts = [251, 503, 753, 1005] #index of the first business day, 2011-2014
bdays = [252, 250, 252, 251] # number of business days, 2011-2014
malen = 200 #length of moving average period
rf = 0.01/100 #risk-free rate
#%%
""" 
    Local functions are defined below
"""
#%% Read in file and forming the database
""" Read in historical adj close data on each date for each stock, forming a dict """
""" Get the available stock universe """
def getStockUniv():
    stockuniv_list = []
    with open('stockuniv.csv', 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            stockuniv_list.append(row[0])
    return stockuniv_list

""" Read historical adj close price data of a single stock """
def readStock(name):
    return pd.read_csv( 'Data/' + name + '.csv', index_col='Date')

""" Construct Database on Adj Price """        
def formDB(stocklist):
    price_db = dict()
    for stock in stocklist:
        stock_df = readStock(stock)
        price_db[stock] = stock_df['Adj Close']
    return price_db

""" Calculate daily return """
def calDailyReturnDB(price_db):
    dreturn_db = dict()
    for name in price_db.keys():
        stockhistory = price_db[name]
        returnhistory = np.zeros(len(stockhistory) - 1) #return list is 1 cell shorter than price list
        for i in range(len(stockhistory) - 1):
            returnhistory[i] = stockhistory[i+1]/stockhistory[i] - 1
        dreturn_db[name] = returnhistory
    return dreturn_db        

""" Calculate Moving Average """
def calMovAvrDB(price_db, malen):
    if malen < 1:
        malen = 5
    if malen > 200:
        malen = 200
    shift = shifts[0]
    mvavr_db = dict()
    for name in price_db.keys():
        stockhistory = price_db[name]
        mahistory = np.zeros(len(stockhistory) - shift - 1) #ma list does not include 2010
        for i in range(len(stockhistory) - shift - 1):
            mahistory[i] = np.average(stockhistory[i+shift-malen:i+shift]) # MA_(t-1)
        mvavr_db[name] = mahistory
    return mvavr_db

#%% Calculate Decile Portfolio Tables
""" Calculate the volatility for each stock at the end of each year """
def calvltTB(dreturn_db):
    vlt_tb = []
    for name in dreturn_db.keys():
        vlt = [name]
        for i in range(4):
            vlt.append(np.std(dreturn_db[name][:shifts[i]], ddof = 1))
        vlt_tb.append(vlt)
    return vlt_tb

""" Calculate volatility decile portfolios """
def calvltDecPorts(vlt_tb):
    vltDecs_ll = []
    declen = len(vlt_tb)/10
    for i in range(4):
        vlt_tb.sort(key = lambda x: x[i+1])
        ranklist = [i[0] for i in vlt_tb]
        vltDec_l = []
        for i in range(9):
            vltDec_l.append(ranklist[i*declen:(i+1)*declen])
        vltDec_l.append(ranklist[9*declen:])
        vltDecs_ll.append(vltDec_l)
    return vltDecs_ll            

#%% Calculate returns
""" Calculate return of a decile portfolio for a specific year, stock-based operation """
def calPortRet(portstock_l, year, price_db, mvavr_db, dreturn_db):
    dailyrets = []    
    shift = shifts[year]
    for i in range(bdays[year]):
        stockrets = []
        for name in portstock_l:
            if price_db[name][i+shift-1] > mvavr_db[name][i+shift-shifts[0]]:
                r = dreturn_db[name][i+shift]
            else:
                r = rf
            stockrets.append(r)
        dailyrets.append(np.average(stockrets))
    return np.average(dailyrets), np.std(dailyrets, ddof = 1)

#""" Calculate return of a decile portfolio for a specific year, port-based operation """
#def calPortRet(portstock_l, year, price_db, mvavr_db, dreturn_db):
#    dailyrets = []    
#    shift = shifts[year]
#    for i in range(bdays[year]):
#        price = 0
#        ma = 0
#        r = 0
#        for name in portstock_l:
#            price += price_db[name][i+shift-1]
#            ma += mvavr_db[name][i+shift-shifts[0]]
#            r += dreturn_db[name][i+shift]
#            """ use equal-weighting """
#        if price > ma:
#            r = r/len(portstock_l)
#        else:
#            r = rf
#        dailyrets.append(r)
#    return np.average(dailyrets), np.std(dailyrets, ddof = 1)

""" Calculate returns for 10 decile portfolios """
def calDecPortRets(price_db, mvavr_db, dreturn_db, vltDecs_ll):      
    MADecsRet_ll = [] 
    MADecsVar_ll = []
    for year in range(4):
        decrets = []
        decvars = []
        for dec in range(10):
            mean, var = calPortRet(vltDecs_ll[year][dec], year, price_db, mvavr_db, dreturn_db)
            decrets.append(mean)
            decvars.append(var)
        MADecsRet_ll.append(decrets) 
        MADecsVar_ll.append(decvars)
    return MADecsRet_ll, MADecsVar_ll

#%% Statistics        
def avrAnlRet(DecsRets, DecsVars):
    Rets = []
    Vars = []
    print "Mean return, Standard Deviations: "
    for i in range(10):
        b = [x[i] for x in DecsRets]
        c = [x[i] for x in DecsVars]
        ret = np.average(b) * 252
        var = np.average(c)*sqrt(252)
        Rets.append(ret)
        Vars.append(var)
        print ret, var
    return Rets, Vars
    
#%% Main Routine 
if __name__ == '__main__':
    start = time.clock()
    stockuniv_list = getStockUniv()
    price_db = formDB(stockuniv_list)
    dreturn_db = calDailyReturnDB(price_db)
    vlt_tb = calvltTB(dreturn_db)
    vltDecsPorts_ll = calvltDecPorts(vlt_tb)
    mvavr_db = calMovAvrDB(price_db, malen)
    MADecsRets, MADecsVars = calDecPortRets(price_db, mvavr_db, dreturn_db, vltDecsPorts_ll)
    Rets, Vars = avrAnlRet(MADecsRets, MADecsVars)
    end = time.clock()
    print "Execution Time: ", end - start