pd.DataFrame(pd.DataFrame())#!/usr/bin/env python3
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

from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize

import unidecode

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)


#let's create a tokenizer:
def simple_tokenizer(text,stopW):
    words = word_tokenize(text)
    print("Tokenized %d Words, now filtering"%len(words))
    
    words = map(lambda word: unidecode.unidecode(word.lower()), words)
    words = [word for word in words if (word not in stopW and word[0] != '/') and word[0] != '\\']
    return words


fileIn = "jsk_datataviz_channel/jsk_dataviz_video.csv"

stop_file = open("stop_words_french.txt", "r")
stop_french = stop_file.read().split("\n")
stupid_file = open("stupid_words_french.txt", "r")
stupid_french = stupid_file.read().split("\n")




stopWords = set(STOPWORDS)

for w in stop_french :
    stopWords.add(w) 
for w in stupid_french :
    stopWords.add(w) 

    
stopWords.add("vidéo") 
stopWords.add("vidéos") 
stopWords.add("video") 
stopWords.add("c'est")
stopWords.add("chaîne")
stopWords.add("chaine")
stopWords.add("youtube")

stopWords.add("https")
stopWords.add("nan")
stopWords.add("live")
stopWords.add("gaming")


df = pd.read_csv(fileIn, index_col=0, on_bad_lines='skip', sep=',',   engine="c")

print("File Read there are {} observations and {} features in this dataset.  \n".format(df.shape[0],df.shape[1]))

# Nettoyage des non-dates à la main
df  = df.drop(df.iloc[367957].name)
df  = df.drop(df.iloc[589823].name)
df  = df.drop(df.iloc[1037272].name)
df  = df.drop(df.iloc[1467866].name)

df['Dates'] = pd.to_datetime(df['video_published_timestamp'], format='%Y-%m-%d %H:%M:%S')
df = df.sort_values(by=['Dates'])

# Nettoyage des non-dates à la main
df = df.iloc[:-45130,:]

print("Saving pickle")
df.to_pickle("filtered.pkl")

g = df.groupby(pd.Grouper(key='Dates', freq='M'))
dfs = [group for _,group in g]

print("Grouped in %d monthes"%len(dfs))

allList = {}
for i, dfM in enumerate(dfs):
    desc = dfM['video_description']
    text = '\n'.join(unidecode.unidecode(str(x).lower()) for x in desc)
    token = simple_tokenizer(text,stopWords)
    print("Computing frequency for month %d"%i)
    fdist = FreqDist(token)
    mostC = fdist.most_common(1000)
    for w,ni in mostC:
        if w in allList.keys():
            allList[w] = allList[w]+int(ni)
        else:
            allList[w] = int(ni)
        
# on enleve ceux qui cmmencent par des apostrophes
newList = {}
for key in allList.keys():
    if(key[1]=="'"):
        if key[2:] in allList.keys():
            newList[key[2:]] = allList[key[2:]]+allList[key]
        else:
            newList[key[2:]] = allList[key]
    else:
        newList[key] = allList[key]
        
            
goodWords = pd.DataFrame.from_dict(newList, orient='index')
goodWords = goodWords.sort_values(by = 0, ascending=False)

with open("goodWords.txt", 'w') as output:
    for i, row in goodWords[:1200].iterrows():
        output.write(str(i) + '\n')

