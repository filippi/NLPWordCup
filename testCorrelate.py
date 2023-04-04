#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 11:05:56 2023

@author: filippi_j
"""


import numpy as np
import pandas as pd
from os import path
import csv
import json


import matplotlib.pyplot as plt

dkw = pd.read_pickle("lastRunAllVids.pk")
dkw['Date'] =  pd.to_datetime(dkw['DateDay'])
dkw.set_index('Date', inplace=True)

selectedK = list(dkw.keys()[:1000])


dcat = pd.DataFrame(index=dkw.index, columns=selectedK+["Date"])
dcat = dcat.fillna(0)
for cat in selectedK:
    dcat[cat] = dkw[cat]*(1)/dkw['NVIDEOS']

print("Read data")
dcat['Date'] = dcat.index
g = dcat.groupby(pd.Grouper(key='Date', freq='2W'))
dfs = [group for _,group in g]   


cKDat = pd.DataFrame(columns=selectedK,index=(range(len(dfs))))
cKDat = cKDat.fillna(0)


for i, dsub in enumerate(dfs):
    for cat in selectedK:
        cKDat[cat][i] = dsub[cat].mean()*100        

print("Compiled data")        
cKDat = cKDat.rolling(2).mean()
cKDat.loc[0] = cKDat.loc[1]

corrKW=cKDat.corr().abs()

corCouples = corrKW.unstack().sort_values(kind="quicksort")

corCouples = corCouples.reset_index()
corCouples.rename(columns = {'level_1':'B'}, inplace = True)
corCouples.rename(columns = {'level_0':'A'}, inplace = True)
corCouples.rename(columns = {0:'p'}, inplace = True)

strange  =corCouples[corCouples['p'].between(.93, .98)]
unstrange  =corCouples[corCouples['p'].between(.01, .02)]

print(unstrange[unstrange["A"] == "macron"], strange[strange["A"] == "macron"])

for i, row in strange.iterrows():
    print(row["A"],row["B"],row["p"])

fun= [ ['vierge', 'partenaire'],
 ['homme', 'seduction'],
 ['qatar', 'couleurs'],
 ['conclusion', 'introduction'],
 ['theorie', 'midas'],
 ['jesus', 'snapchat'],
 ['ukraine', 'cryptos'],
 ['covid-19', 'cuisine']]
for a,b in fun:
    print(a,b)
    cKDat[[a,b]].plot()
    

