import os
import folium
import numpy as np
import geopandas
from pprint import pprint
import json
import pandas as pd

# Définir les couleurs attribuée à chacun des partis ayant 
# fait élire au moins 1 personne comme députée
couleurs = {
    'C.A.Q.-É.F.L.': 'lightblue',
    'P.L.Q./Q.L.P.': 'red',
    'Q.S.': 'orange',
    'P.Q.': 'blue'
}

# Utilisons les données publiées par le DGEQ pour extraire
# les résultats pour chacune des circonscriptons
dgeq2018_path = os.path.join('data', 'resultats.json')
dgeq2018_file = open(dgeq2018_path)
dgeq2018_json = json.load(dgeq2018_file)

#On commence avec un tables vide
resultats_par_circonscripton = []

# Que l'on remplit avec les données lues
# Pour chaque circonscription:
# On crée un dictionnaire (c_res)
# On ajoute le code identifiant la circonscripton (CO_CEP)
# Le parti vainqueur dans cette circonscripton (vainqueur)
# Et la couleur associée à ce parti.
for c in dgeq2018_json['circonscriptions']:
    c_res = {
        'CO_CEP': int(c['numeroCirconscription']),
        'vainqueur': c['candidats'][0]['abreviationPartiPolitique'],
        'couleur': couleurs[c['candidats'][0]['abreviationPartiPolitique']]
    }
    # Enfin on ajoute le dictionnaire c_rest au tableau des résultats
    resultats_par_circonscripton.append(c_res)


# Enfin, à l'aide du tableau, on crée un "dataFrame" à l'aide de la
# blibliothèque pandas.
resultats_df = pd.DataFrame(resultats_par_circonscripton)
resultats_df.set_index('CO_CEP', inplace=True)



#Utilison sles données publuiées par le DGEQ pour extraire
#les limites territoriales de chacune des circonscripton
#le résultat (circonscriptons) est un dataframe créé par
#la bibliotèque geopandas
circ_path = os.path.join('data', 'circ.json')
circonscriptions = geopandas.read_file(circ_path)
circonscriptions.set_index('CO_CEP', inplace=True)

#Enfin fusionnons les deux dataframes pour avoir en même temps
#les limites territoriales et les résultats des élections du
#1er octobre 2018
r2 = circonscriptions.join(resultats_df)

#Créons une carte géographique centrée sur le Québec
m = folium.Map([46, -73.5], tiles='stamentoner', zoom_start=8)

# Et ajoutons une couche supplémentaire conduite par le
# dataframe r2
folium.GeoJson(r2,
    style_function=lambda dd: {
        'fillColor': dd['properties']['couleur'],
        'color' : 'green',
        'weight' : 1.5,
        'fillOpacity' : 0.7,
        },
    tooltip = folium.features.GeoJsonTooltip(fields=['NM_CEP'], labels=False)

    ).add_to(m)

#Enfin sauvegardons la carte
quebec_html = os.path.join('html', 'quebec.html')
m.save(quebec_html)
