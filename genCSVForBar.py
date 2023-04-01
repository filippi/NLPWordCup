#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 09:49:42 2023

@author: Jean-Baptiste Filippi - Alberto Alonso-Pinar
Challenge dataviz 2023 

Processing final du fichier pour en sortir des synthèses graphiques et en CVS pour la bar chart race


"""

import numpy as np
import pandas as pd
from os import path

allVids.read_pickle("lastRunAllVids.pk")
#name,value,year,lastValue,rank

# dans cette dataframe, une colonne par mot clé +

kwStart = 10
kwLimit = 50

 
 
with open('test.csv',  'w', newline='') as csvfile:
    mycsvwriter = csv.writer(csvfile, delimiter=',')
    mycsvwriter.writerow(["name","value","year","lastValue","rank"])
    
    for index, row in allVids.iterrows():
        
        rankedRow = row.sort_values(ascending=False)
        
        for ni, keyRow in enumerate(rankedRow[kwStart:kwStart+kwLimit].keys()):
            lastValue=rankedRow[keyRow]
            if(index>0):
                lastValue=allVids.loc[index-1][keyRow]
            mycsvwriter.writerow([keyRow,rankedRow[keyRow],float(2020+(0.1*index)),lastValue,ni+1])
    
 


 
