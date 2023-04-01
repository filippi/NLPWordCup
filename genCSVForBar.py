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

dkw = pd.read_pickle("lastRunAllVids.pk")
#name,value,year,lastValue,rank

import matplotlib.pyplot as plt

# dans cette dataframe, une colonne par mot clé (+1000) + une colonne par nb vue mot clé + une colonne par nb comment mot clé + une colonne ppour la date
dkw = pd.read_pickle("lastRunAllVids.pk")

dkw['Date'] =  pd.to_datetime(dkw['DateDay'])
dkw.set_index('Date', inplace=True)

categories={}
categories["Film"] = ["comedie","filme","film","cinema","acteurs","tournage"]
categories["Automobile"] = ["voiture","auto","dakar","electrique"]
categories["Musique"] = ["musique","skyrock","guitare","guitare"]
categories["Animaux"] = ["chat","chiennete","animaux"]
categories["Sports"] = ["mercato","goal","champions","pronostics","musculation","mbappe","sport","sportive","football","barca","psg", "chelsea","madrid"]
categories["Voyage et événements"] = ["barcelone","usa","evenement","aventures","aventure","vacances","qatar"]
categories["Gaming"] = ["jeu","fifa","fortnite" ,"league","streaming", "playstation","games","gameplay","gta","roblox"]
categories["Divertissement"] = ["cuisine","livre", "camera", "culture", "theatre", "podcast", "comedie", "cinema", "lectures", "magazine"]
categories["Politique"] = ["guerre","actualite", "international","analyse", "interview", "immigration", "nationale", "analyses" ]
categories["Beauté"] = ["horoscope","nutrition", "beauty", "astuce", "newsletter", "boutique", "meditation", "gossip'afrique", "coaching" ]
categories["Education "] = ["education", "tech", "techniques","technique","digital", "energies", "logiciel", "formation", "electrique"]
categories["Associatif"] = ["jesus","famille", "dimanche", "social", "projet", "membres", "enfants", "priere","chretienne" ]
categories["Actualites"] = ["ukraine", "covid-19", "macron", "journalistes", "coronavirus", "financier", "president", "russie", "btc","politique" ,"russe"]


dcat = pd.DataFrame(index=dkw.index, columns=list(categories.keys()))
dcat = dcat.fillna(0)

for cat in categories:
    for catKW in categories[cat]:
        dcat[cat] = dcat[cat] + ((dkw[catKW]*(1+dkw[catKW+"NV"]))/dkw['NVIDEOS'])

dcat.plot()
    
    



#"coronavirus" "covid-19" 
#chelsea

kwStart = 10
kwLimit = 50

 
 
with open('test.csv',  'w', newline='') as csvfile:
    mycsvwriter = csv.writer(csvfile, delimiter=',')
    mycsvwriter.writerow(["name","value","year","lastValue","rank"])
    
    for index, row in *.iterrows():
        
        rankedRow = row.sort_values(ascending=False)
        
        for ni, keyRow in enumerate(rankedRow[kwStart:kwStart+kwLimit].keys()):
            lastValue=rankedRow[keyRow]
            if(index>0):
                lastValue=allVids.loc[index-1][keyRow]
            mycsvwriter.writerow([keyRow,rankedRow[keyRow],float(2020+(0.1*index)),lastValue,ni+1])
    
 


 
