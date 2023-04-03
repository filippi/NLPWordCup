#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 13:45:34 2023

@author: filippi_j
"""

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
import csv
import json


import matplotlib.pyplot as plt

# dans cette dataframe, une colonne par mot clé (+1000) + une colonne par nb vue mot clé + une colonne par nb comment mot clé + une colonne ppour la date


categories={}
categories["Film"] = ["comedie","filme","film","cinema","acteurs","tournage"]
categories["Automobile"] = ["voiture","auto","dakar","electrique","moto"]
categories["Musique"] = ["musique","skyrock","guitare","chansons"]
categories["Animaux"] = ["chat","chiennete","animaux"]
categories["Sports"] = ["mercato","goal","champions","pronostics","musculation","mbappe","sport","sportive","football","barca","psg", "chelsea","madrid"]
categories["Voyages"] = ["barcelone","usa","evenement","aventures","aventure","vacances","qatar"]
categories["Gaming"] = ["jeu","lol","fifa","league","streaming", "playstation","games","gameplay","gta","roblox","minecraft"] # "fortnite"
categories["Divertissement"] = ["cuisine","livre", "camera", "culture", "theatre", "podcast", "comedie", "cinema", "lectures", "magazine"]
categories["Politique"] = ["guerre","actualite", "international","analyse", "interview", "immigration", "nationale", "analyses" ,"poutine","politique" ]
categories["Beaute"] = ["horoscope","nutrition", "beauty", "astuce", "newsletter", "boutique", "meditation", "gossip'afrique", "coaching" ]
categories["Education"] = ["education", "tech", "techniques","technique","digital", "energies", "logiciel", "formation", "electrique"]
categories["Associatif"] = ["jesus","famille", "dimanche", "social", "projet", "membres", "enfants", "priere","chretienne","argent" ]
categories["Actualites"] = ["ukraine", "covid-19", "macron", "journalistes", "coronavirus", "financier", "president", "russie", "btc","russe"]
categories["Clubs_foot"] = ["marseille","liverpool","barca","psg", "chelsea","madrid","manchester","monaco","om","bayern"]
categories["Fortnite"] = ["fortnite"]



def genCSVforWeb(fname, listOfKeys, dfs):
    allVids = pd.DataFrame(columns=listOfKeys,index=(range(len(dfs))))
    allVids = allVids.fillna(0)
    
    for i, dsub in enumerate(dfs):
        for cat in listOfKeys:
            allVids[cat][i] = dsub[cat].mean()*100
    
    allVids = allVids.rolling(2).mean()
    allVids.loc[0] = allVids.loc[1]
    
    
    
    with open("data/"+fname+".csv",  'w', newline='') as csvfile:
        mycsvwriter = csv.writer(csvfile, delimiter=',')
        mycsvwriter.writerow(["name","value","year","lastValue","rank"])
        
        for index, row in allVids[1:].iterrows():
            
            rankedRow = row.sort_values(ascending=False)
            
            for ni, keyRow in enumerate(rankedRow.keys()):
                lastValue=rankedRow[keyRow]
                if(index>0):
                    lastValue=allVids.loc[index-1][keyRow]
                mycsvwriter.writerow([keyRow,rankedRow[keyRow],index,lastValue,ni+1])
    
    with open("data/"+fname+"_p.csv",  'w', newline='') as csvfile:
        mycsvwriter = csv.writer(csvfile, delimiter=',')
        mycsvwriter.writerow(["name","year","frequency"])
        
        for index, row in allVids[1:].iterrows():
            for k in row.keys():
                mycsvwriter.writerow([k,index,int(row[k]*100)])
        
    
 

dkw = pd.read_pickle("lastRunAllVids.pk")

dkw['Date'] =  pd.to_datetime(dkw['DateDay'])
dkw.set_index('Date', inplace=True)

dcat = pd.DataFrame(index=dkw.index, columns=list(categories.keys()))
dcat = dcat.fillna(0)

for cat in categories:
    for catKW in categories[cat]:
        dcat[cat] = dcat[cat] + (dkw[catKW]*(1))/dkw['NVIDEOS']

dcat['Date'] = dcat.index
g = dcat.groupby(pd.Grouper(key='Date', freq='2W'))
dfs = [group for _,group in g]   

listOfKeys = list(categories.keys())
fname="categories"

genCSVforWeb(fname, listOfKeys, dfs)

for cat in categories:
    listOfKeys = categories[cat]
    dcat = pd.DataFrame(index=dkw.index, columns=listOfKeys)
    dcat = dcat.fillna(0)

    for catKW in listOfKeys:
        dcat[catKW] = dcat[catKW] + (dkw[catKW]*(1))/dkw['NVIDEOS']

    dcat['Date'] = dcat.index
    g = dcat.groupby(pd.Grouper(key='Date', freq='2W'))
    dfs = [group for _,group in g]   
    
    fname=cat

    genCSVforWeb(fname, listOfKeys, dfs)



colors = ["paleturquoise","palevioletred","papayawhip","peru","pink","plum","powderblue","red","rosybrown","royalblue","salmon","sandybrown","seagreen","silver","skyblue","slateblue","slategray","slategrey","snow","springgreen","steelblue","tan","teal","thistle","tomato","turquoise","violet","wheat","white","whitesmoke"]

allColors={}
catColors={}
for i,cat in enumerate(categories):    
    allColors[cat] = colors[i]
    catColors[cat] = colors[i]
    
for cat in categories:    
    for i,scat in enumerate(categories[cat]):    
        allColors[scat] = colors[i]


with open('catcolors.js', 'w') as f:
    f.write("var allColors = ")
    json.dump(allColors, f)
    f.write("\n var catColorsData = [")
    json.dump(catColors, f)
    f.write("];\n var colors = "+str(colors))
 

