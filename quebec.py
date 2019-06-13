import os
import folium
import numpy as np
import geopandas
from pprint import pprint
import json
import pandas as pd

couleurs = {
    'C.A.Q.-É.F.L.': 'lightblue',
    'P.L.Q./Q.L.P.': 'red',
    'Q.S.': 'orange',
    'P.Q.': 'blue'
    
}
dgeq2018_path = os.path.join('results', 'resultats.json')
dgeq2018_file = open(dgeq2018_path)
dgeq2018_json = json.load(dgeq2018_file)

resultats_par_circonscripton = []
for c in dgeq2018_json['circonscriptions']:
    c_res = {
        'CO_CEP': int(c['numeroCirconscription']),
        'vainqueur': c['candidats'][0]['abreviationPartiPolitique'],
        'couleur': couleurs[c['candidats'][0]['abreviationPartiPolitique']]
    }
    resultats_par_circonscripton.append(c_res)


resultats_df = pd.DataFrame(resultats_par_circonscripton)
resultats_df.set_index('CO_CEP', inplace=True)




circ_path = os.path.join('results', 'circ.json')
circonscriptions = geopandas.read_file(circ_path)
circonscriptions.set_index('CO_CEP', inplace=True)

r2 = circonscriptions.join(resultats_df)

m = folium.Map([46, -73.5], tiles='stamentoner', zoom_start=8)
folium.GeoJson(r2,
    style_function=lambda dd: {
        'fillColor': dd['properties']['couleur'],
        'color' : 'black',
        'weight' : 0.5,
        'fillOpacity' : 0.5,
        }
    ).add_to(m)
m.save(nam_of_the_file)
