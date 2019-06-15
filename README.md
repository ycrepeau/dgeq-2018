# dgeq-2018
Résultats des élections générales 

« Comprend des données ouvertes octroyées sous la licence d'utilisation des données ouvertes du directeur général des élections disponible à l'adresse Web dgeq.org. L'octroi de la licence n'implique aucune approbation par le directeur général des élections de l'utilisation des données ouvertes qui en est faite. »

Montréal : ogr2ogr -clipsrc -73.7 45.4 -73.2 45.7 montreal.json sections.json
Québec:    ogr2ogr -clipsrc -71.75 46.7 -70.75 47.0 quebec.json sections.json
Rouyn:      ogr2ogr -clipsrc -79.5 45.0 -72.0 52.0 rouyn.json sections.json
