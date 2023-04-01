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

 

good_file = open("goodWords.txt", "r")
good_french = good_file.read().split("\n")

goodWords = set()

for w in good_french :
    goodWords.add(w) 

df = pd.read_pickle("filtered.pkl")

g = df.groupby(pd.Grouper(key='Dates', freq='1D'))
dfs = [group for _,group in g]

print("Grouped in %d elements"%len(dfs))



allCollumnNames= list(goodWords)
allCollumnNamesAndNV = [itm+"NV" for itm in allCollumnNames]
allCollumnNamesAndNC  = [itm+"NC" for itm in allCollumnNames]

allVids = pd.DataFrame(columns=allCollumnNames+allCollumnNamesAndNV+allCollumnNamesAndNC+["NVIDEOS","DateDay"],index=(range(len(dfs))))
allVids = allVids.fillna(0)


for i, dfM in enumerate(dfs):
    allVids.loc[i]["NVIDEOS"] = len(dfM)
    allVids.loc[i]["DateDay"] = dfM["Dates"].iloc[0].value
    print("computed %d on %d - %d elements"%(i,len(dfs),len(dfM)),dfM["Dates"].iloc[0].strftime('%Y-%m-%d'),allVids.loc[i]["DateDay"])
    for index, row in dfM.iterrows():
        text = str(row['video_description'])+ str(row['video_name'])
        nv = float(row['video_views']) 
        nc = float(row['video_comments'])
        token = simple_tokenizer( unidecode.unidecode(text.lower()),goodWords)
        for lk,lv in FreqDist(token).most_common(1000):
            allVids.loc[i][lk] += lv 
            allVids.loc[i][lk+"NV"] += nv
            allVids.loc[i][lk+"NC"] += nc
    
    
allVids.to_pickle("lastRunAllVids.pk")

 
