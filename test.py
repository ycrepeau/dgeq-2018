import os
import folium
import numpy as np
import geopandas
from pprint import pprint
import json
import pandas as pd
import re
import math

#Regex pour vérifier si S.V =  5A, 5B, 5C...
re_sv = re.compile('(\d+)([A-Z]*)')

# Fonctions utilitaires
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

def getStrength(d):
  max = 0
  strength = 0.0
  total_votes = d['B.V.']
  if total_votes == 0: 
    #pprint("BV = 0 pour {}".format(d))
    return 0.0

  try: 
    p =d
    if (p['pq']== p['pq'] and p['pq'] > max):
      max = p['pq']
    if (p['plq'] == p['plq'] and p['plq'] > max):
      max = p['plq']
    if p['caq']== p['caq'] and p['caq'] > max:
      max = p['caq']
    if p['qs']== p['qs'] and  p['qs'] > max:
      max = p['qs']
  except:
    max = 0

  pourcent_votes = max/total_votes

  if 0.0 <= pourcent_votes < 0.2: strength = 0.2
  if 0.2 <= pourcent_votes < 0.3: strength = 0.3
  if 0.3 <= pourcent_votes < 0.4: strength = 0.4
  if 0.4 <= pourcent_votes < 0.5: strength = 0.5
  if 0.5 <= pourcent_votes <= 1.0: strength = 0.65

  return strength
  
def groupe_consolidation(d):
  reponse = ''
  m = re_sv.match(d)
  #print("d: {} m: {}".format(d,m.group(1)))
  if len(m.group(2)) > 0: reponse = m.group(1)
  return reponse




# Identification des partis 
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
  #'104', #Mégantic
  #'110', #Saint-François
  #'116', #Sherbrooke 
  #'120', #Orford
  #'126', #Johnson
  #'132', #Richmond
  #'138', #Drummond-Bois-Franc
  #'144', #Arthabasca
  #'150', #Nicolet-Bétancour

  # Montérégie
  #'204', #Brome-Missisquoi
  #'206', #Granby
  #'210', #Iberville
  #'212', #Saint-Jean
  #'216', #Huntingdon
  #'218', #Beauharnois
  #'220', #Soulanges
  #'224', #Vaudreuil
  #'226', #Châteauguay
  #'230', #Sanguinet
  #'232', #La Prairie
  #'236', #Lapinière
  #'238', #Chambly
  #'240', #Vachon
  #'244', #Laporte
  #'246', #Marie-Victorin
  #'250', #Taillon
  #'252', #Montarville
  #'256', #Verchère
  #'258', #Borduas
  #'260', #Saint-Hyacinthe
  #'264', #Richelieu

  # 300-399 Ile de Montréal
  '300', #Verdun
  '304', #Marguerite-Bourgeoys
  '306', #Marquette
  '310', #Jacques Cartier
  '312', #Nelligan
  '316', #Robert-Badwin
  '318', #Saint-Laurent
  '320', #D'Arcee-McGee
  '324', #Notre-Dame-de-Grace
  '326', #Saint-Henri Saint-Anne
  '330', #Sainte-Marie - Saint-Jacques
  '332', #Westmount Saint-Louis
  '336',
  '338',
  '340',
  '344',
  '346',
  '350',
  '352',
  '356',
  '360',
  '364',
  '366',
  '370',
  '380',
  '390', 
  '358', 
  
  # 400-499 Laval
  '460', #Chomeydeu
  '466', #Fabre
  '454', #Laval des Rapides
  '482', #Mille Isles
  '470', #Sainte-Rose
  '476', #Vimont

  #500-599 Laurentides
  #'502', #Groulx
  #'508', #Deux-Montagne
  #'514', #Mirabel
  #'520', #Argenteuil
  #'530', #Saint-Jérôme
  #'526', #Les Plaines
  #'536', #Blainville
  #'542', #Terrebonne
  #'548', #Masson
  #'554', #L'Assomption
  #'560', #Repentigny
  #'566', #Berthier
  #'570', #Joliette
  #'576', #Rousseau
  #'582', #Prévost
  #'588', #Bertrand
  #'594', #Labelle

  # 600-699 Outaouais
  #'602', #Hull
  #'608', #Pontiac
  #'614', # Gatineau
  #'620', #Chapleau
  #'626', #Papineau
  #'636', #Rouyn-Noranda
  #'648', #Abitibi-Est
  #'642', #Abitibi-Ouest
  #'660', #Trois-Rivières 
  #'666', #Maskinongé
  #'670', #Laviolette - Saint-Maurice
  #'676', #Champlain
  #
  # 700-799 Québec
  #'714',  #Portneuf
  #'930', #Roberval
  #'938' #Ungave
]

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
#pprint(sections.shape[0])
#pprint(sections.columns.values.tolist())

df_internes = sections[sections['CO_CEP'].isin(couverture)]
sections = df_internes
sections.set_index(['CO_CEP', 'S.V.'], inplace=True, drop=False)


center_x = sections['geometry'].unary_union.centroid.x
center_y = sections['geometry'].unary_union.centroid.y
bounds = sections['geometry'].total_bounds

#print("bounds: {} center_x: {} center_y: {}".format(bounds, center_x, center_y))

m = folium.Map([center_y, center_x], tiles='stamentoner', zoom_start=9)
m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

cumul = pd.DataFrame()

for co_cep in couverture:
  res_path = os.path.join('data', 'resultats-section-vote', "%s.csv"%co_cep)
  data = pd.read_csv(res_path, sep=';', encoding='latin1', dtype={'S.V.':'str', 'Code':'str'})
  data.dropna(subset=['S.V.'], inplace=True)
  data['S.V.'] = data['S.V.'].astype(str)
  data.rename(columns={"Code":"CO_CEP", 'Nom des Municipalités':'NM_MUNI'}, inplace=True)
  
  #Consolidation 5A, 5B, 5C... ici.
  data['consolidation'] = data['S.V.'].apply(groupe_consolidation)
  data_subset = data[data['consolidation'] != '']
  data_subset.set_index(['CO_CEP','S.V.'], inplace=True)
  #pprint(data_subset)
  data_consolide = data_subset.groupby('consolidation').agg({'Circonscription':'first', 'B.V.':'sum', 'B.R.':'sum'})
  #pprint(data_consolide)
  
  data.set_index(['CO_CEP','S.V.'], inplace=True, drop=False)
  #pprint(data)
  
  candidats_list = data.columns.tolist()
  ei_pos = candidats_list.index('É.I.')
  bv_pos = candidats_list.index('B.V.')
  #print("ei: {} bv: {}".format(ei_pos, bv_pos))
  candidats = candidats_list[ei_pos+1:bv_pos]
  
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
      print("WARNING: candidat:'{}' not matched".format(candidat))
      data.drop(labels=candidat, axis=1, inplace=True)

  data.drop(labels=['Circonscription', 'Date scrutin', 'Étendue', 'Secteur', 'Regroupement', 'É.I.'], axis=1, inplace=True)
  
  #Consolidation 5A, 5B, 5C... ici.
  # Sélectionner les rangée correspondants aux sections subdivisées (A, B C...)
  data['consolidation'] = data['S.V.'].apply(groupe_consolidation)
  
  
  data_subset = data[data['consolidation'] != '']
  data_subset.set_index(['CO_CEP','S.V.'], inplace=True, drop=False)
  #pprint(data_subset)
  f = dict.fromkeys(data_subset, 'sum')
  f.pop('consolidation', None)
  f.pop('S.V.', None)
  f['CO_CEP'] = 'first'
  f['NM_MUNI'] = 'first'

  data_consolide = data_subset.groupby('consolidation', as_index=False).agg(f)
  data_consolide.rename(columns={'consolidation':'S.V.'}, inplace=True)
  data_consolide.set_index(['CO_CEP','S.V.'], inplace=True, drop=False)

  #pprint(data_consolide)
  
  if (cumul.size <= 0):
    cumul = data
  else:
    a = cumul.append(data, sort=False)
    cumul = a

  if data_consolide.size > 0:
    a = cumul.append(data_consolide, sort=False)
    cumul = a


striped = cumul[['plq', 'pq', 'caq', 'qs', 'B.V.', 'NM_MUNI']]
sections = sections.join(striped)
sections['couleur']  = sections.apply(getColor, axis=1)
sections['strength'] = sections.apply(getStrength, axis=1)


sections.set_index(['CO_CEP', 'S.V.'], inplace=True, drop=False)
#pprint(sections[['plq', 'pq', 'caq', 'qs', 'couleur', 'strength' ,'NM_MUNI']])


folium.GeoJson(sections,
  tooltip = folium.features.GeoJsonTooltip(fields=['NM_CEP', 'S.V.', 'NM_MUNI', 'qs', 'caq', 'plq', 'pq'], labels=True),
  style_function=lambda dd: {
      'fillColor': dd['properties']['couleur'],
      'color' : 'green',
      'weight' : 0.25,
      'fillOpacity' : dd['properties']['strength'],
      },

).add_to(m)


region_test_html = os.path.join('docs', 'region_test.html')
m.save(region_test_html)