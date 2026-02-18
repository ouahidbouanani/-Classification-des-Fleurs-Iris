# 🌸 Projet Classification des Fleurs Iris avec MongoDB

**Python 3.13.2** | UCI ML Repository | Kaggle | MongoDB | Machine Learning

## 📋 Description

Projet complet d'analyse et classification des fleurs Iris utilisant MongoDB et Machine Learning.
Implémente toutes les parties demandées (1-4) avec support multi-sources de données.

## 🎯 Parties Implémentées

✅ **Partie 1** : Analyse statistique descriptive  
✅ **Partie 2** : Visualisation des données  
✅ **Partie 3** : Régression simple et multiple  
✅ **Partie 4** : Classification supervisée + Prototype interactif  
✅ **MongoDB** : Modélisation NoSQL et optimisation  

## 🚀 Installation Rapide

```bash
# Installer les dépendances
pip install -r requirements.txt

# Démarrer MongoDB (terminal séparé)
mongod --dbpath ./data/db

# Exécuter le projet complet
python run_all.py
```

## 📊 Exécution par Parties

```bash
# Partie 1 & 2 : Analyse et Visualisation
python src/partie1_2_analyse_visualisation.py

# Partie 3 : Régression
python src/partie3_regression.py

# Partie 4 : Classification + MongoDB
python src/partie4_classification_mongodb.py

# Dashboard interactif
streamlit run src/dashboard_interactif.py
```

## 📁 Structure

```
iris_classification_complet/
├── src/
│   ├── partie1_2_analyse_visualisation.py
│   ├── partie3_regression.py
│   ├── partie4_classification_mongodb.py
│   ├── dashboard_interactif.py
│   └── utils/
│       ├── data_loader.py
│       ├── mongo_helper.py
│       └── ml_helper.py
├── outputs/
│   ├── exploratory/
│   ├── models/
│   └── reports/
├── data/db/
└── run_all.py
```

## 🎓 Livrables

- ✅ Analyses statistiques complètes
- ✅ 15+ visualisations professionnelles
- ✅ Modèles de régression (simple & multiple)
- ✅ 5 modèles de classification (>95% accuracy)
- ✅ Base MongoDB optimisée
- ✅ Dashboard interactif Streamlit

## 📖 Documentation

Voir les commentaires détaillés dans chaque script Python.

Bon projet ! 🌸
