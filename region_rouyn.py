import os
import folium
import numpy as np
import geopandas
from pprint import pprint
import json
import pandas as pd
import re
import math

def getColor(d):
  max = 0
  color = 'gray'
  try: 
    p =d
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
    color = 'white'

  return color

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


couverture = [
  # 100-199 Estrie Centre-du-Québec
  '104', #Mégantic
  '110', #Saint-François
  '116', #Sherbrooke 
  '120', #Orford
  '126', #Johnson
  '132', #Richmond
  '138', #Drummond-Bois-Franc
  '144', #Arthabasca
  '150', #Nicolet-Bétancour

  # Montérégie
  '204', #Brome-Missisquoi
  '206', #Granby
  '210', #Iberville
  '212', #Saint-Jean
  '216', #Huntingdon
  '218', #Beauharnois
  '220', #Soulanges
  '224', #Vaudreuil
  '226', #Châteauguay
  '230', #Sanguinet
  '232', #La Prairie
  '236', #Lapinière
  '238', #Chambly
  '240', #Vachon
  '244', #Laporte
  '246', #Marie-Victorin
  '250', #Taillon
  '252', #Montarville
  '256', #Verchère
  '258', #Borduas
  '260', #Saint-Hyacinthe
  '264', #Richelieu

  # 300-399 Ile de Montréal
  # 400-499 Laval

  #500-599 Laurentides
  '502', #Groulx
  '508', #Deux-Montagne
  '514', #Mirabel
  '520', #Argenteuil
  '530', #Saint-Jérôme
  '526', #Les Plaines
  '536', #Blainville
  '542', #Terrebonne
  '548', #Masson
  '554', #L'Assomption
  '560', #Repentigny
  '566', #Berthier
  '570', #Joliette
  '576', #Rousseau
  '582', #Prévost
  '588', #Bertrand
  '594', #Labelle

  # 600-699 Outaouais
  '602', 
  '608', 
  '614', 
  '620', 
  '626', 
  '636',
  '648',
  '642', 
  '660', 
  '666', 
  '670', 
  '676', 
  '714', 
  '930', 
  '938']


# Donnees géographiques des sections de vote.
#Utilison sles données publuiées par le DGEQ pour extraire
#les limites territoriales de chacune des circonscripton
#le résultat (circonscriptons) est un dataframe créé par
#la bibliotèque geopandas
circ_path = os.path.join('data', 'rouyn.json')
sections = geopandas.read_file(circ_path)
sections['NO_SV'].astype('str')
sections['CO_CEP'].astype('str')
sections.rename(columns={'NO_SV':'S.V.'}, inplace=True)
pprint(sections.shape[0])
pprint(sections.columns.values.tolist())

df_internes = sections[sections['CO_CEP'].isin(couverture)]
sections = df_internes
sections.set_index(['CO_CEP', 'S.V.'], inplace=True, drop=False)

pprint(sections.shape[0])
#pprint(sections)

m = folium.Map([48.5, -78], tiles='stamentoner', zoom_start=8)

cumul = pd.DataFrame()

for co_cep in couverture:
  res_path = os.path.join('data', 'resultats-section-vote', "%s.csv"%co_cep)
  data = pd.read_csv(res_path, sep=';', encoding='latin1', dtype={'S.V.':'str', 'Code':'str'})
  data.dropna(subset=['S.V.'], inplace=True)
  data.rename(columns={"Code":"CO_CEP", 'Nom des Municipalités':'NM_MUNI'}, inplace=True)
  data.set_index(['CO_CEP','S.V.'], inplace=True)
  
  
  candidats = data.columns.tolist()[7:-3]
  pprint(candidats)
  
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
      print("WARNING: candidat:{} not matched".format(candidat))
      data.drop(labels=candidat, axis=1, inplace=True)

  data.drop(labels=['Circonscription', 'Date scrutin', 'Étendue', 'Secteur', 'Regroupement', 'É.I.'], axis=1, inplace=True)
  if (cumul.size <= 0):
    cumul = data
  else:
    a = cumul.append(data, sort=False)
    cumul = a

pprint(cumul.dtypes)
striped = cumul[['plq', 'pq', 'caq', 'qs', 'NM_MUNI']]
sections = sections.join(striped)
#pprint(sections.dtypes)
sections['couleur'] = sections.apply(getColor, axis=1)
sections.set_index(['CO_CEP', 'S.V.'], inplace=True, drop=False)
pprint(sections[['plq', 'pq', 'caq', 'qs', 'couleur', 'NM_MUNI']])


folium.GeoJson(sections,
    tooltip = folium.features.GeoJsonTooltip(fields=['NM_CEP', 'S.V.', 'couleur', 'NM_MUNI'], labels=True),
    style_function=lambda dd: {
        'fillColor': dd['properties']['couleur'],
        'color' : 'green',
        'weight' : 0.25,
        'fillOpacity' : 0.5,
        },

    ).add_to(m)


#Enfin sauvegardons la carte
region_rouyn_html = os.path.join('docs', 'region_rouyn.html')
m.save(region_rouyn_html)
