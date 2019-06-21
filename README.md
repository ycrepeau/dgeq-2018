# dgeq-2018
Résultats des élections générales 

« Comprend des données ouvertes octroyées sous la licence d'utilisation des données ouvertes du directeur général des élections disponible à l'adresse Web dgeq.org. L'octroi de la licence n'implique aucune approbation par le directeur général des élections de l'utilisation des données ouvertes qui en est faite. »


Voir https://ycrepeau.github.io/dgeq-2018 pour explications.

- Montréal : ogr2ogr -clipsrc -73.7 45.4 -73.2 45.7 montreal.json sections.json
- Québec:    ogr2ogr -clipsrc -71.75 46.7 -70.75 47.0 quebec.json sections.json
- Rouyn:      ogr2ogr -clipsrc -79.5 45.0 -72.0 52.0 rouyn.json sections.json
- Sherbrooke: ogr2ogr -clipsrc -72.5 45.0 -64.0 52.0 sherbrooke.json sections.json

Pour enlever de tres gros fichiers du git:

git filter-branch --tree-filter 'rm -rf data/sections.json' HEAD
