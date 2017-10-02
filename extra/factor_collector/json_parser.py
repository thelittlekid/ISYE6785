# -*- coding: utf-8 -*-
"""
Created on Sat Aug 01 16:39:15 2015

@author: fantasie
"""
import json
import os
import csv
import time

#%% Global Variables
data_dir = 'Data/'
markets = ['sz', 'ss']
factor_set = ['PE', 'PB', 'PCF', 'PS', 'OperatingProfitRatio']
csv_postfix = '_factor.csv'
#%% Local functions are defined below
""" Find the specific format files which ends with endstring """
def endWith(*endstring):
    ends = endstring
    def run(s):
        f = map(s.endswith,ends)
        if True in f: return s
    return run

""" Check if data is available for all factors """
def checkFactors(factor_set, item):
    for factor in factor_set:
        if not factor in item.keys():
            return False
    return True
#%% Main Routine
if __name__ == '__main__':
    start = time.clock()
    workdirs = [data_dir + market + '/' for market in markets]
    for workdir in workdirs:        
        list_file = os.listdir(workdir)
        a = endWith('.txt')
        txtlist = []
        f_file = filter(a,list_file)
        for i in f_file:
            txtlist.append(i[:-4])
#           print i, i[:-4]
    
        for name in txtlist:
            jstring = open(workdir + name + '.txt').read()
            jdict = json.loads(jstring)
            records = []
            title = ['tradeDate']
            for factor in factor_set:
                title.append(factor)
            records.append(title)
            if jdict['retMsg'] == 'Success':
                for item in jdict['data']:
                    dailyrecord = []
                    if checkFactors(factor_set, item):
#                    if 'PB' in item.keys() and 'PCF' in item.keys() and 'PE' in item.keys() and 'PS' in item.keys():
#                        dailyrecord = [item['tradeDate'], item['PB'], item['PCF'], item['PE'], item['PS']]
                        dailyrecord = []
                        for field in title:
                            dailyrecord.append(item[field])
                        records.append(dailyrecord)
                writer = csv.writer(open(workdir + name + csv_postfix, 'wb'))
                for item in records:
                    writer.writerow(item)
    del writer
    end = time.clock()
    print "Execution time: ", end - start