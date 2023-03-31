# NLPWordCup - Course de mots-clés pour le challenge Dataviz / Université di Corsica Pasquale Paoli 2023

- Les mots des commentaires des chaines et vidéos, leurs fréquences
- Données Jellysmack Keywords/Channels/Videos 

## L'idée
Une grande partie du travail a été d'extraire les données des 1.6 Go de texte bien formatés, puis d'en faire une projection se prêtant à l'analyse.
Nous avons choisi 4 étapes intermédiaires:
    - Une première pour trouver les mots à ne pas inclure, mais aussi parser les fichiers,  ce qui a permit de trouver :
    - les mots à inclure, qu'il a quand même fallu filtrer, on a donc une liste de 1000+ mots les plus fréquents
    - pour chacun de ces mots, on calcule une fréquence sur chaque entrée (vidéo/chaine), on en fait un sous ensemble (avec la frequence et nb vue)
    - enfin on extrait de cette dataframe (1.5 millions d'enregistrements) des résumés par mois, et on synthétise dans un fichier 

Nous appliquons la même idée pour les chaînes youtube et leur description. 
## Utilisation
Cloner le dépôt et ouvrir index.html avec Google Chrome. Aussi sur https://filippi.github.io/NLPWordCup/

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