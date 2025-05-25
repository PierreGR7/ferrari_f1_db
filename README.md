# Ferrari F1 Dashboard

Ce projet propose un tableau de bord interactif des performances historiques de l'écurie Ferrari en Formule 1, basé sur les données publiques de l'API Ergast Developer.

L'objectif est de construire un pipeline complet de data engineering :
- Extraction et transformation des résultats de course depuis 1950
- Stockage relationnel structuré dans une base SQLite
- Visualisation via un dashboard Streamlit interactif

## Base de données

La base `ferrari_f1.db` contient les tables suivantes :
- `drivers`
- `constructors`
- `circuits`
- `races`
- `results`
Les données sont récupérées depuis l'API Ergast, avec pagination complète pour garantir l'exhaustivité de l'historique.

Ce projet utilise SQLite comme moteur de base de données relationnelle. SQLite est léger, sans configuration, et parfaitement adapté pour un projet personnel ou un tableau de bord à utilisateur unique.

## Fonctionnalités du dashboard

- Total de points, victoires, podiums, abandons
- Évolution des performances par saison
- Classement des pilotes Ferrari par points cumulés
- Filtre interactif pour explorer les performances d’un pilote

## Installation

git clone https://github.com/PierreGR7/ferrari_f1_db.git
cd ferrari_f1_db
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python etl_ferrari.py
streamlit run dashboard/app.py

## Auteur

Pierre Graef
https://www.pierregraef.com/
graef.pierre@gmail.com

