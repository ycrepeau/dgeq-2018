import os
import folium
import numpy as np
import geopandas
from pprint import pprint
import json
import pandas as pd
import re
import math

couleurs = {
    'C.A.Q.-É.F.L.': 'lightblue',
    'P.L.Q./Q.L.P.': 'red',
    'Q.S.': 'orange',
    'P.Q.': 'blue'
}

re_caq = re.compile('.*C\.A\.Q\.-É\.F\.L\.$')
re_qs = re.compile('.*Q\.S\.$')
re_plq = re.compile('.*P\.L\.Q\./Q\.L\.P\.$')
re_pq = re.compile('.* P\.Q\.$')
re_pvq = re.compile('.*P\.V\.Q\./G\.P\.Q\.$')
re_pmlq = re.compile('.* P\.M\.L\.Q\.$')
re_pcq = re.compile('.* P.C.Q./C.P.Q.$')
re_npdq = re.compile('.* N\.P\.D\.Q.$')
re_bp = re.compile('.* B\.P\.$')
re_ea = re.compile('.* É\.A\.$')
re_pn = re.compile('.* P\.N\.$')


couverture = [304,306,310,312,316,318,320,324,326,330,336,338,340,344,346,350,352,356,360,364,366,370,380,390]
# Donnees géographiques des sections de vote.
#Utilison sles données publuiées par le DGEQ pour extraire
#les limites territoriales de chacune des circonscripton
#le résultat (circonscriptons) est un dataframe créé par
#la bibliotèque geopandas
circ_path = os.path.join('data', 'montreal.json')
sections = geopandas.read_file(circ_path)
sections['NO_SV'].astype('str')
sections['CO_CEP'].astype('str')
sections.set_index(['CO_CEP', 'NO_SV'], inplace=True, drop=False)



m = folium.Map([45.5, -73.6], tiles='stamentoner', zoom_start=12)

cumul = pd.DataFrame()

for co_cep in couverture:
  res_path = os.path.join('data', 'resultats-section-vote', "%d.csv"%co_cep)
  data = pd.read_csv(res_path, sep=';', encoding='latin1', dtype={'S.V.':'str', 'Code':'str'})
  data.dropna(subset=['S.V.'], inplace=True)
  data.rename(columns={"Code":"CO_CEP"}, inplace=True)
  data.set_index(['CO_CEP','S.V.'], inplace=True)
  
  
  candidats = data.columns.tolist()[7:-2]
  
  for candidat in candidats:
    if re_caq.match(candidat): 
      data.rename(columns={candidat:'caq'}, inplace=True)
    elif re_qs.match(candidat): 
      data.rename(columns={candidat:'qs'}, inplace=True)
    elif re_plq.match(candidat): 
      data.rename(columns={candidat:'plq'}, inplace=True)
    elif re_pq.match(candidat): 
      data.rename(columns={candidat:'pq'}, inplace=True)
    elif re_pvq.match(candidat): 
      data.rename(columns={candidat:'pvq'}, inplace=True)
    elif re_pmlq.match(candidat): 
      data.rename(columns={candidat:'pmlq'}, inplace=True)
    elif re_pcq.match(candidat): 
      data.rename(columns={candidat:'pcq'}, inplace=True)
    elif re_npdq.match(candidat): 
      data.rename(columns={candidat:'npdq'}, inplace=True)
    elif re_bp.match(candidat): 
      data.rename(columns={candidat:'bp'}, inplace=True)
    elif re_ea.match(candidat): 
      data.rename(columns={candidat:'ea'}, inplace=True)
    elif re_pn.match(candidat): 
      data.rename(columns={candidat:'pn'}, inplace=True)
    else:
      data.drop(labels=candidat, axis=1, inplace=True)

  data.drop(labels=['Circonscription', 'Date scrutin', 'Étendue', 'Nom des Municipalités', 'Secteur', 'Regroupement', 'É.I.'], axis=1, inplace=True)
  if (cumul.size <= 0):
    cumul = data
  else:
    a = cumul.append(data, sort=False)
    cumul = a

striped = cumul[['plq', 'pq', 'caq', 'qs']]
sections = sections.join(striped)
pprint(sections.dtypes)

def getColor(d):
  max = 0
  color = 'gray'
  try: 
    p = d['properties']
    if (p['pq']== p['pq'] and p['pq'] > max):
      max = p['pq']
      color = 'blue'
    if (p['plq'] == p['plq'] and p['plq'] > max):
      max = p['plq']
      color = 'red'
    if p['caq']== p['caq'] and p['caq'] > max:
      max = p['caq']
      color = 'lightblue'
    if p['qs']== p['qs'] and  p['qs'] > max:
      max = p['qs']
      color = 'orange'
  except:
    color = 'gray'

  return color

folium.GeoJson(sections,
    tooltip = folium.features.GeoJsonTooltip(fields=['NM_CEP', 'NO_SV'], labels=True),
    style_function=lambda dd: {
        'fillColor': getColor(dd),
        'color' : 'green',
        'weight' : 0.5,
        'fillOpacity' : 0.7,
        },

    ).add_to(m)


#Enfin sauvegardons la carte
region_montreal_html = os.path.join('html', 'region_montreal.html')
m.save(region_montreal_html)
