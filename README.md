# NLPWordCup - Course de mots-clés pour le challenge Dataviz / Université di Corsica Pasquale Paoli 2023

- Les mots des commentaires des chaines et vidéos, leurs fréquences
- Données Jellysmack Keywords/Channels/Videos 



## L'idée
Une grande partie du travail a été d'extraire les données des 1.6 Go de texte bien formatés, puis d'en faire une projection se prêtant à l'analyse.
Nous avons choisi 4 étapes intermédiaires:
* Une première pour trouver les mots à ne pas inclure, mais aussi parser les fichiers,  ce qui a permit de trouver :
* les mots à inclure, qu'il a quand même fallu filtrer, on a donc une liste de 1000+ mots les plus fréquents
* pour chacun de ces mots, on calcule une fréquence sur chaque entrée (vidéo/chaine), on en fait un sous ensemble (avec la frequence et nb vue)
* enfin on extrait de cette dataframe (1.5 millions d'enregistrements) des résumés par mois, et on synthétise dans un fichier 

Nous appliquons la même idée pour les chaînes youtube et leur description.

## Utilisation
Cloner le dépôt et ouvrir index.html avec Google Chrome.
Aussi disponible sur https://filippi.github.io/NLPWordCup/


## Description detaillée

### Introduction

Les données fournies sont reparties dans trois fichiers différents:
* un fichier contenant les catégories genérales des vidéos YouTube (ie : "sports", "gaming", "tutoriels" etc). La liste contenait environ 90 catégories différentes.
* un fichier contenant des chaînes youtube : leur nom, la date de création, le nombre d'abonnés et la description de la chaîne. Ce fichier contient environ 60000 chaînes différentes pour la période 2005-2023.
* un fichier contenant la liste des vidéos téléchargés sur la plateforme : la date de création, le nombre de visualisations, le nombre de commentaires. Ce fichier contient environ 600000 entrées pour la période 2020-2023.
	
### Pre processing



#### Les catégories: ####

La liste de catégories était assez importante avec presque 90 choix différents pour classer les vidéos. La première étape était donc de simplifier cette liste pour n'en garder qu'une liste courte mais assez représentative. 
La liste finale contient donc les catégories suivantes :
* Film
* Automobile
* Musique
* Sports
* Animaux
* Voyages et événements
* Gaming
* Divertissement
* Politique
* Style et beauté
* Science et education
* Associatif
* Actualités

A l'aide d'une intelligence avancée nous avons ensuite determiné les mots des descriptions des vidéos youtube (provenant du pre traitement réalisé sur le ficher vidéos) les plus représentatifs de chaque catégorie.
Ceci nous a fourni 10 mots par catégorie. Avec cette liste on peut donc automatiquement determiner la categorie d'une vidéo en fonction des mots utilisés dans la description.
Par exemple, les mots qui décrivent correctement la categorie Gaming sont :
* "discord","twitch","jeu","fifa", "fortnite","league","streaming", "playstation","games","gameplay"

## Technos
- D3.js -> pour la visualisation en course de Barchart
- Panda -> Traitement et filtrage des données
- nltk -> Traitement des mots/statistiques
- Wordcloud -> pour l'expérimentaiton vidéo sur les mots clés en nuage de mots/matplotlib


## La ou on a pompé les morceaux de code
Merci à vous :
- Fork de https://github.com/ytdec/bar-chart-race pour les Bar Charts

## L'équipe
- **Alberto Alonso Pinar**, Valladolid, voit mieux de près, python noob
- **Jean-Baptiste Filippi**, Corte, voit mieux de loin, python

## fichiers
- filterWords.py : calcule les occurence de tous les mots en enlevant les mots que nous ne voulont pas, pour trouver les mots que l'on veut
- goodWords.txt :
- goodWordsWithDate.py : re-parse les fichiers et sort la fréquence de chaque mot pour entrée datée (ligne) + globalement la pupularité de l'entrée 
- compileSynthesis.py : fabrique le fichier pour affichace js
- stop_words_french.txt : les mots génériques que nous ne voulons pas
- stupid_words_french.txt : les mots spécifiques que nous ne voulons pas, issus du traitement des video_channels