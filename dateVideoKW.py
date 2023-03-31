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

from nltk.corpus import stopwords

from nltk.tokenize import word_tokenize

import unidecode

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)


#let's create a tokenizer:
def simple_tokenizer(text,yesW):
    words = word_tokenize(text)
    print("Tokenized %d Words, now filtering"%len(words))
    
    words = map(lambda word: unidecode.unidecode(word.lower()), words)
    words = [word for word in words if word in yesW ]
    return words


fileIn = "jsk_datataviz_channel/jsk_dataviz_video.csv"

good_file = open("goodWords.txt", "r")
good_french = good_file.read().split("\n")

goodWords = set()

for w in good_french :
    if(w[1]=="'"):
        print(w) 

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


g = df.groupby(pd.Grouper(key='Dates', freq='M'))
dfs = [group for _,group in g]

print("Grouped in %d monthes"%len(dfs))

allList = {}
for i, dfM in enumerate(dfs[:2]):
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
        



exit(0)

desc = df['video_description']
text = '\n'.join(str(x) for x in desc)


desc = df['channel_description'][1110:1210]
text = '\n'.join(str(x) for x in desc)
token = simple_tokenizer(text)

fdist = FreqDist(token)
fdist1 = fdist.most_common(10000)[00:10]
allText = ""
for word, count in fdist1:
    if(len(word) > 3):
        allText = allText + "%s,"%word * count


df['Dates'] = pd.to_datetime(df['video_published_timestamp'], format='%Y-%m-%d %H:%M:%S')

wc = WordCloud(max_words=1000, stopwords=stopWords, margin=10,
               random_state=1).generate(text)

plt.figure( figsize=(40,20), facecolor='k')
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig('wordcloud.png', facecolor='k', bbox_inches='tight')


print(len(text), fdist1)
default_colors = wc.to_array()
plt.title("Custom colors")
plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3),
           interpolation="bilinear")
 
