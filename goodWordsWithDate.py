#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 09:49:42 2023

@author: Jean-Baptiste Filippi - Alberto Alonso-Pinar
Challenge dataviz 2023 

Preprocessing inputs to find good keywords

"""

import numpy as np
import pandas as pd
import re
from os import path
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import random
import csv
from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize

import unidecode

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)


#let's create a tokenizer:
def simple_tokenizer(text,yesW):
    words = word_tokenize(text)
    words = [word for word in words if len(word) > 2 ]
    words = [word[2:] if word[1]=="'" else word for word in words]
    words = [word for word in words if word in yesW ]
    return words


fileIn = "../jsk_datataviz_channel/jsk_dataviz_video.csv"

good_file = open("goodWords.txt", "r")
good_french = good_file.read().split("\n")

goodWords = set()

for w in good_french :
    goodWords.add(w) 

df = pd.read_pickle("filtered.pkl")

g = df.groupby(pd.Grouper(key='Dates', freq='36D'))
dfs = [group for _,group in g]

print("Grouped in %d tenth of year"%len(dfs))


allCollumnNames= list(goodWords)
allVids = pd.DataFrame(columns=allCollumnNames,index=(range(len(dfs))))
allVids = allVids.fillna(0)


for i, dfM in enumerate(dfs):
    print(i)
    for index, row in dfM[:5000].iterrows():
        text = row['video_description']
        token = simple_tokenizer( unidecode.unidecode(str(text).lower()),goodWords)
        for lk,lv in FreqDist(token).most_common(1000):
            allVids.loc[i][lk] += lv 

 
#name,value,year,lastValue,rank
#Apple,214480,2018,211447.400000003,1
#Apple,211447.400000003,2017.9,208414.799999999,1
kwStart = 0
kwLimit = 50

#statsVids = pd.DataFrame(columns=["name","value","year","lastValue","rank"],index=(range(1+len(dfs)*kwLimit)))
#statsVids = statsVids.fillna(0)
 
 
with open('test.csv',  'w', newline='') as csvfile:
    mycsvwriter = csv.writer(csvfile, delimiter=',')
    mycsvwriter.writerow(["name","value","year","lastValue","rank"])
    
    for index, row in allVids.iterrows():
        
        rankedRow = row.sort_values(ascending=False)
        
        for ni, keyRow in enumerate(rankedRow[kwStart:kwStart+kwLimit].keys()):
            lastValue=rankedRow[keyRow]
            if(index>0):
                lastValue=allVids.loc[index-1][keyRow]
            mycsvwriter.writerow([keyRow,rankedRow[keyRow],float(2021+(0.1*index)),lastValue,ni+1])
    
 


 
