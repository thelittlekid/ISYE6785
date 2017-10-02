# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 10:10:59 2015

@author: fantasie
"""
import csv
import time
import os
from dataapi import Client

#%% Global Variables
markets = ['sz', 'ss']
factor_set = ['PE', 'PB', 'PCF', 'PS', 'OperatingProfitRatio']
begin_date = '20100103'
end_date = '20150731'
data_dir = 'Data/'
ticker_file_prefix = 'stockuniv_'
univ_file = 'stocks_'
err_file = 'errorlist_'
puase_sec = 30
pause_count = 200
url_prefix = '/api/market/getStockFactorsDateRange.json?field=tradeDate'
token = '2f0699fff9af6cec368a1af2fe7c4bd8fe64d09cb9096a55257fd1b0c4f0c199'
#%% Local functions are defined below
""" Refresh connecntion """
def refresh(client, pause_sec):
    time.sleep(pause_sec)
    print 'sleeping'
    client = Client()
    client.init(token)
    
    
""" Check and create market folder """
def checkMarket(market):
    if not os.path.exists(data_dir + market):
        os.makedirs(data_dir + market)

""" Write 'log file' """
def writelogfile(stockuniv, errorstock, market):
    writer = csv.writer(open( data_dir + univ_file + market + '.csv', 'wb'))
    for item in stockuniv:
        writer.writerow([item])
    writer = csv.writer(open( data_dir + err_file + market + '.csv', 'wb'))
    for item in errorstock:
        writer.writerow([item])
    del writer

#%% Main Routine
if __name__ == "__main__":
    start = time.clock()
    for factor in factor_set:
        url_prefix = url_prefix + ',' + factor
    """ Initialize Client """
    client = Client()
    client.init(token)
    
    i = 1 # counter for stocks
    for market in markets:
        checkMarket(market) 
        stockuniv = [] #  list of stocks that can be successfully downloaded
        errorstock = [] # list of stocks that can't be downloaded
        stocklist = csv.reader(file(data_dir + ticker_file_prefix + market + '.csv', 'rb'))
        for stock in stocklist:
            if i%pause_count == 0:
                refresh(client, puase_sec)
            name = stock[0].split('.')[0]            
            url = url_prefix + '&secID=&ticker=' + name \
                  + '&beginDate=' + begin_date + '&endDate=' + end_date
            try:
                code, result = client.getData(url)
                i = i+1
                if code == 200:
                    file_object = open(data_dir + market + '/' + name + '.' + market + '.txt', 'w')
                    file_object.write(result)
                    file_object.close()
                    stockuniv.append(name + '.' +  market)
                else:
                    print code
            except Exception, e:
                errorstock.append(name + '.' + market)
#                raise e
        writelogfile(stockuniv, errorstock, market)        
    end = time.clock()
    print 'Execution time: ', end - start