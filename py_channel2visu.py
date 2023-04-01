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

import csv


#%%

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


#%%

pathfile = "C:/Users/Alberto/Documents/jellysmack/repo2/NLPWordCup/"
fileIn = pathfile+"jsk_datataviz_channel.csv"




#%%


stop_file = open(pathfile+"stop_words_french.txt", "r")
stop_french = stop_file.read().split("\n")
stupid_file = open(pathfile+"stupid_words_french.txt", "r")
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

#%%

good_file = open(pathfile+"goodWords.txt", "r")
good_french = good_file.read().split("\n")

goodWords = set()

for w in good_french :
    if(w[1]=="'"):
        print(w) 

df = pd.read_csv(fileIn, sep=';')

print("File Read there are {} observations and {} features in this dataset.  \n".format(df.shape[0],df.shape[1]))

df['Dates'] = pd.to_datetime(df['channel_created_timestamp'], format='%Y-%m-%d %H:%M:%S')
df = df.sort_values(by=['Dates'])

df.drop(df[df['channel_name'] == 'YouTube'].index, inplace = True) #drop youtube channel


df.to_pickle(pathfile+"filtered.pkl")


g = df.groupby(pd.Grouper(key='Dates', freq='M'))
dfs = [group for _,group in g]

print("Grouped in %d monthes"%len(dfs))

allList = {}
for i, dfM in enumerate(dfs):
    desc = dfM['channel_description']
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
        




#%%

def simple_tokenizer(text,yesW):
    words = word_tokenize(text)
    words = [word for word in words if len(word) > 2 ]
    words = [word[2:] if word[1]=="'" else word for word in words]
    words = [word for word in words if word in yesW ]
    return words

 

good_file = open(pathfile+"verygoodWords.txt", "r")
good_french = good_file.read().split("\n")

goodWords = set()

for w in good_french :
    goodWords.add(w) 

df = pd.read_pickle(pathfile+"filtered.pkl")

g = df.groupby(pd.Grouper(key='Dates', freq='90D'))
dfs = [group for _,group in g]

print("Grouped in %d tenth of year"%len(dfs))


allCollumnNames= list(goodWords)
allVids = pd.DataFrame(columns=allCollumnNames,index=(range(len(dfs))))
allVids = allVids.fillna(0)


for i, dfM in enumerate(dfs):
    print(i)
    #print(dfM)
    #print('---')
    for index, row in dfM[:5000].iterrows():
        text = row['channel_description']
        token = simple_tokenizer( unidecode.unidecode(str(text).lower()),goodWords)
        for lk,lv in FreqDist(token).most_common(1000):
            allVids.loc[i][lk] += lv 

 
#name,value,year,lastValue,rank
#Apple,214480,2018,211447.400000003,1
#Apple,211447.400000003,2017.9,208414.799999999,1
kwStart = 0
kwLimit = 15

#statsVids = pd.DataFrame(columns=["name","value","year","lastValue","rank"],index=(range(1+len(dfs)*kwLimit)))
#statsVids = statsVids.fillna(0)
 
 
with open(pathfile+'test_channel.csv',  'w', newline='') as csvfile:
    mycsvwriter = csv.writer(csvfile, delimiter=',')
    mycsvwriter.writerow(["name","value","year","lastValue","rank"])
    
    for index, row in allVids.iterrows():
        
        rankedRow = row.sort_values(ascending=False)
        
        for ni, keyRow in enumerate(rankedRow[kwStart:kwStart+kwLimit].keys()):
            lastValue=rankedRow[keyRow]
            if(index>0):
                lastValue=allVids.loc[index-1][keyRow]
            mycsvwriter.writerow([keyRow,rankedRow[keyRow],float(2005+(0.1*index)),lastValue,ni+1])
            
            


#%%

#desc = df['channel_description']
#text = '\n'.join(str(x) for x in desc)
#
#
##desc = df['channel_description'][1110:1210]
##text = '\n'.join(str(x) for x in desc)
#token = simple_tokenizer(text)
#
#fdist = FreqDist(token)
#fdist1 = fdist.most_common(10000)[0:10]
#allText = ""
#for word, count in fdist1:
#    if(len(word) > 3):
#        allText = allText + "%s,"%word * count
#
#
#df['Dates'] = pd.to_datetime(df['channel_created_timestamp'], format='%Y-%m-%d %H:%M:%S')
#
#wc = WordCloud(max_words=1000, stopwords=stopWords, margin=10,
#               random_state=1).generate(text)
#
#plt.figure( figsize=(40,20), facecolor='k')
#plt.imshow(wordcloud)
#plt.axis("off")
#plt.tight_layout(pad=0)
#plt.savefig('wordcloud.png', facecolor='k', bbox_inches='tight')
#
#
#print(len(text), fdist1)
#default_colors = wc.to_array()
#plt.title("Custom colors")
#plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3),
#           interpolation="bilinear")