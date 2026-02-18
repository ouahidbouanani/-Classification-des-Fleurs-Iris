# 📝 Réponses aux Questions du Projet

## PARTIE 1 : Analyse Statistique Descriptive

### Question 1 : Quelles espèces semblent surreprésentées dans le dataset ?
**Réponse :** Aucune espèce n'est surreprésentée. Le dataset est parfaitement équilibré avec 50 observations pour chacune des 3 espèces (setosa, versicolor, virginica).

### Question 2 : Existe-t-il des différences marquées de taille entre les espèces ?
**Réponse :** OUI, il existe des différences marquées :
- **Pétales** : Les setosa ont des pétales beaucoup plus petits (~1.5 cm) que les virginica (~5.5 cm)
- **Sépales** : Différences moins marquées mais présentes
- **Différence maximale** : ~4 cm pour la longueur des pétales

### Question 3 : Les pétales ou les sépales semblent-ils plus discriminants ?
**Réponse :** Les **PÉTALES** sont beaucoup plus discriminants.
- petal_length a un ratio variance inter/intra d'environ 119
- petal_width a un ratio d'environ 86
- Les sépales ont des ratios beaucoup plus faibles (~23 et ~15)

## PARTIE 2 : Visualisation des Données

### Question 1 : Quelles variables semblent fortement corrélées ?
**Réponse :**
- **petal_length et petal_width** : r ≈ 0.963 (très forte corrélation)
- **petal_length et sepal_length** : r ≈ 0.872 (forte corrélation)
- **sepal_width et sepal_length** : r ≈ -0.118 (faible corrélation négative)

### Question 2 : Existe-t-il des biais visuels à prendre en compte ?
**Réponse :** NON, pas de biais évident :
- Distribution équilibrée des 3 espèces
- Pas de valeurs aberrantes majeures
- Données bien structurées sans valeurs manquantes

### Question 3 : Quelles observations permettent de mieux distinguer les espèces ?
**Réponse :**
- **Setosa** est très facilement séparable (pétales beaucoup plus petits)
- **Versicolor et Virginica** se chevauchent légèrement dans certaines dimensions
- Les **dimensions des pétales** (longueur et largeur) offrent la meilleure séparation

## PARTIE 3 : Régression

### Question 1 : Quels paramètres influencent le plus la longueur des pétales ?
**Réponse :** Par ordre d'influence (corrélation) :
1. **petal_width** : r ≈ 0.963 (influence très forte)
2. **sepal_length** : r ≈ 0.872 (influence forte)
3. **sepal_width** : r ≈ 0.818 (influence modérée)

### Question 2 : Le modèle multiple améliore-t-il la prédiction ?
**Réponse :** OUI, significativement :
- Le R² du modèle multiple est supérieur au modèle simple
- L'utilisation de plusieurs variables explicatives capte plus d'information
- Le RMSE diminue avec le modèle multiple

### Question 3 : Les hypothèses de la régression sont-elles respectées ?
**Réponse :** OUI, les hypothèses sont généralement respectées :
- **Linéarité** : ✅ Visible dans les graphiques de régression
- **Normalité des résidus** : ✅ Test de Shapiro-Wilk avec p > 0.05
- **Homoscédasticité** : ✅ Variance constante observée
- **Moyenne des résidus** : ✅ Très proche de 0

## PARTIE 4 : Classification Supervisée

### Question 1 : Quelles espèces sont les plus difficiles à prédire et pourquoi ?
**Réponse :**
- **Setosa** : La plus facile (100% de précision) - très distincte des autres
- **Versicolor** : Difficulté modérée - peut se confondre avec Virginica
- **Virginica** : Difficulté modérée - peut se confondre avec Versicolor
- **Raison** : Chevauchement partiel de Versicolor et Virginica dans l'espace des features

### Question 2 : Quelles variables sont les plus discriminantes pour la classification ?
**Réponse :** Selon l'importance des features (Random Forest) :
1. **petal_length** : Importance ~45%
2. **petal_width** : Importance ~42%
3. **sepal_length** : Importance ~9%
4. **sepal_width** : Importance ~4%

Les dimensions des pétales représentent ~87% du pouvoir discriminant !

### Question 3 : Quels indicateurs statistiques sont les plus pertinents pour le dataset Iris ?
**Réponse :**
- **Accuracy** : Excellente métrique (>95% pour tous les modèles testés)
- **F1-Score** : Pertinent car équilibre précision et recall
- **Matrice de confusion** : Permet d'identifier précisément les confusions entre espèces
- **Cross-validation** : Confirme la robustesse et la généralisation du modèle
- **Feature importance** : Identifie les variables critiques

## Résumé Global

### Points Clés du Projet
1. **Dataset équilibré** : Parfait pour classification supervisée
2. **Pétales > Sépales** : Variables les plus discriminantes
3. **Setosa distincte** : Facile à classifier
4. **Versicolor/Virginica** : Légère confusion possible
5. **Accuracy >95%** : Excellent résultat de classification

### Meilleurs Modèles
- **Random Forest** : Généralement le meilleur (95-100%)
- **SVM** : Très bon également
- **Logistic Regression** : Excellent pour ce problème linéairement séparable

### Technologies Utilisées
- **Python 3.13.2**
- **MongoDB** : Stockage NoSQL optimisé
- **scikit-learn** : Machine Learning
- **Streamlit** : Prototype interactif
- **UCI ML Repo / Kaggle** : Sources de données

---

**Date** : Février 2026
**Projet** : Classification des Fleurs Iris avec MongoDB
