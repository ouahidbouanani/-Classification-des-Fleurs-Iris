# 🚀 Démarrage Rapide - Projet Iris Classification

## Installation (2 minutes)

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Installer sources de données (optionnel)
pip install ucimlrepo kagglehub
```

## Exécution Complète (1 commande)

```bash
# Exécuter TOUTES les parties automatiquement
python run_all.py
```

## Exécution Par Parties

```bash
# Parties 1 & 2 : Analyse + Visualisation
python src/partie1_2_analyse_visualisation.py

# Partie 3 : Régression
python src/partie3_regression.py

# Partie 4 : Classification + MongoDB
python src/partie4_classification_mongodb.py

# Prototype Interactif (Partie 4)
streamlit run src/dashboard_interactif.py
```

## MongoDB (Optionnel)

```bash
# Démarrer MongoDB (terminal séparé)
mongod --dbpath ./data/db

# Puis exécuter partie 4
python src/partie4_classification_mongodb.py
```

## Résultats

Après exécution, consultez :
- `outputs/exploratory/` - 9+ visualisations
- `outputs/models/` - Modèles ML sauvegardés
- Dashboard web sur http://localhost:8501

## Support

- Voir README.md pour plus de détails
- Commentaires détaillés dans chaque script

Bon projet ! 🌸
