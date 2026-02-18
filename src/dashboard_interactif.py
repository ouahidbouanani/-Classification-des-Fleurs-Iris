"""
PARTIE 4 - PROTOTYPE INTERACTIF
Dashboard Streamlit pour Classification des Fleurs Iris
Données chargées depuis MongoDB Atlas
Usage: streamlit run src/dashboard_interactif.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.mongo_helper import MongoHelper
from utils.ml_helper import IrisMLHelper

# Configuration
st.set_page_config(page_title="Iris Classification", page_icon="🌸", layout="wide")
'''
@st.cache_data
def load_data_from_mongodb():
    """Charge les données depuis sklearn (TEST)"""
    from sklearn.datasets import load_iris
    
    iris = load_iris()
    df = pd.DataFrame(iris.data, 
                      columns=['sepal_length','sepal_width','petal_length','petal_width'])
    df['species'] = pd.Categorical.from_codes(iris.target, 
                                               ['setosa','versicolor','virginica'])
    df['prediction'] = None
    df['confidence'] = None
    df['model'] = None
    
    return df
'''
def load_data_from_mongodb():
    """Charge les données depuis MongoDB Atlas"""
    mongo = MongoHelper()
    documents = list(mongo.collection.find())
    
    records = []
    for doc in documents:
        records.append({
            'sepal_length': doc['features']['sepal_length'],
            'sepal_width': doc['features']['sepal_width'],
            'petal_length': doc['features']['petal_length'],
            'petal_width': doc['features']['petal_width'],
            'species': doc['species'],
            'prediction': doc.get('prediction', None),
            'confidence': doc.get('confidence', None),
            'model': doc.get('model', None)
        })
    
    mongo.close()
    return pd.DataFrame(records)


@st.cache_resource
def load_model():
    ml = IrisMLHelper()
    df = load_data_from_mongodb()
    X_train, X_test, y_train, y_test = ml.prepare_data(df)
    ml.train_all_models(X_train, y_train)
    ml.evaluate_models(X_test, y_test)
    return ml

# Charger données et modèle depuis MongoDB
df = load_data_from_mongodb()
ml_helper = load_model()

# En-tête
st.title("🌸 Classification des Fleurs Iris - Prototype Interactif")
st.markdown("**Partie 4 : Application Interactive de Classification**")
st.success(f"✅ Connecté à MongoDB Atlas | {len(df)} documents chargés depuis la base de données")
st.markdown("---")

# Sidebar - Navigation
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Choisir une fonction", [
    "📊 Visualisation Variables",
    "🔍 Corrélations",
    "🎯 Prédiction",
    "📈 Séparation Espèces"
])

# PAGE 1 : Visualisation Variables
if page == "📊 Visualisation Variables":
    st.header("📊 Choisir une Variable à Visualiser")
    
    # Sélection variable
    variable = st.selectbox("Variable à analyser", 
                           ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])
    
    # Type de graphique
    graph_type = st.radio("Type de graphique", ["Histogramme", "Boxplot"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"{graph_type} de {variable}")
        
        if graph_type == "Histogramme":
            fig, ax = plt.subplots(figsize=(8, 6))
            for species in df['species'].unique():
                data = df[df['species']==species][variable]
                ax.hist(data, alpha=0.6, label=species, bins=15)
            ax.set_xlabel(variable)
            ax.set_ylabel('Fréquence')
            ax.set_title(f'Distribution de {variable}')
            ax.legend()
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            plt.close()
        else:  # Boxplot
            fig, ax = plt.subplots(figsize=(8, 6))
            df.boxplot(column=variable, by='species', ax=ax)
            ax.set_xlabel('Espèce')
            ax.set_ylabel(variable)
            ax.set_title(f'Boxplot de {variable}')
            st.pyplot(fig)
            plt.close()
    
    with col2:
        st.subheader(f"Statistiques de {variable}")
        stats = df.groupby('species')[variable].agg(['mean', 'std', 'min', 'max'])
        st.dataframe(stats, width="stretch")
        
        st.subheader("Distribution Générale")
        st.write(df[variable].describe())

# PAGE 2 : Corrélations
elif page == "🔍 Corrélations":
    st.header("🔍 Visualiser les Corrélations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        var1 = st.selectbox("Variable X", 
                           ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'], 
                           index=2)
    with col2:
        var2 = st.selectbox("Variable Y", 
                           ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'], 
                           index=3)
    
    # Scatter plot
    st.subheader(f"Corrélation : {var1} vs {var2}")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    for species in df['species'].unique():
        data = df[df['species']==species]
        ax.scatter(data[var1], data[var2], label=species, alpha=0.7, s=100, 
                  edgecolors='black', linewidth=0.5)
    ax.set_xlabel(var1)
    ax.set_ylabel(var2)
    ax.set_title(f'{var1} vs {var2} par espèce')
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close()
    
    # Coefficient de corrélation
    corr_value = df[[var1, var2]].corr().iloc[0, 1]
    st.metric("Coefficient de corrélation", f"{corr_value:.4f}")
    
    # Matrice complète
    st.subheader("Matrice de Corrélation Complète")
    feature_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    corr_matrix = df[feature_cols].corr()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
               square=True, fmt='.3f', ax=ax)
    ax.set_title('Matrice de Corrélation')
    st.pyplot(fig)
    plt.close()

# PAGE 3 : Prédiction
elif page == "🎯 Prédiction":
    st.header("🎯 Prédire l'Espèce d'une Fleur")
    
    st.markdown("""
    Ajustez les curseurs pour saisir les mesures d'une fleur et obtenez une prédiction.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📏 Mesures de la Fleur")
        
        sepal_length = st.slider("Longueur sépale (cm)", 4.0, 8.0, 5.8, 0.1)
        sepal_width = st.slider("Largeur sépale (cm)", 2.0, 4.5, 3.0, 0.1)
        petal_length = st.slider("Longueur pétale (cm)", 1.0, 7.0, 4.3, 0.1)
        petal_width = st.slider("Largeur pétale (cm)", 0.1, 2.5, 1.3, 0.1)
    
    with col2:
        st.subheader("🎯 Prédiction")
        
        # Prédire
        X_input = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        y_pred = ml_helper.best_model.predict(X_input)
        proba = ml_helper.best_model.predict_proba(X_input)
        
        predicted_species = ml_helper.inv_label_map[y_pred[0]]
        
        st.success(f"**Espèce prédite : {predicted_species.upper()} 🌸**")
        
        st.write("**Confiance du modèle :**")
        for i, species in enumerate(['setosa', 'versicolor', 'virginica']):
            st.progress(float(proba[0][i]), text=f"{species}: {proba[0][i]*100:.1f}%")
        
        st.info(f"Modèle utilisé : {ml_helper.best_model_name}")
    
    # Fleurs similaires
    st.markdown("---")
    st.subheader("🔍 Fleurs Similaires dans le Dataset")
    
    features = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']].values
    distances = np.linalg.norm(features - X_input, axis=1)
    df_with_dist = df.copy()
    df_with_dist['distance'] = distances
    
    similar = df_with_dist.nsmallest(5, 'distance')
    st.dataframe(similar[['sepal_length', 'sepal_width', 'petal_length',
                         'petal_width', 'species', 'distance']],
                width="stretch")

# PAGE 4 : Séparation Espèces
elif page == "📈 Séparation Espèces":
    st.header("📈 Observer la Séparation des Espèces")
    
    st.markdown("""
    Visualisez comment les différentes variables séparent les espèces.
    """)
    
    # Variables à comparer
    col1, col2 = st.columns(2)
    with col1:
        var_x = st.selectbox("Variable X", 
                            ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'],
                            index=2, key='sep_x')
    with col2:
        var_y = st.selectbox("Variable Y", 
                            ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'],
                            index=3, key='sep_y')
    
    # Graphique de séparation
    fig, ax = plt.subplots(figsize=(12, 8))
    
    colors = {'setosa': 'red', 'versicolor': 'blue', 'virginica': 'green'}
    for species in df['species'].unique():
        data = df[df['species']==species]
        ax.scatter(data[var_x], data[var_y], 
                  label=species, alpha=0.7, s=150,
                  c=colors[species], edgecolors='black', linewidth=1)
    
    ax.set_xlabel(var_x, fontsize=14)
    ax.set_ylabel(var_y, fontsize=14)
    ax.set_title(f'Séparation des Espèces : {var_x} vs {var_y}', fontsize=16, fontweight='bold')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    plt.close()
    
    # Analyse de séparation
    st.subheader("📊 Analyse de Séparation")
    
    col1, col2, col3 = st.columns(3)
    
    for idx, species in enumerate(df['species'].unique()):
        data = df[df['species']==species]
        
        with [col1, col2, col3][idx]:
            st.metric(f"{species.capitalize()}", f"{len(data)} fleurs")
            st.write(f"**{var_x}:**")
            st.write(f"  Min: {data[var_x].min():.2f}")
            st.write(f"  Max: {data[var_x].max():.2f}")
            st.write(f"  Moy: {data[var_x].mean():.2f}")
            
            st.write(f"**{var_y}:**")
            st.write(f"  Min: {data[var_y].min():.2f}")
            st.write(f"  Max: {data[var_y].max():.2f}")
            st.write(f"  Moy: {data[var_y].mean():.2f}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🌸 Projet Classification Iris - Partie 4 : Prototype Interactif</p>
    <p>Données chargées depuis MongoDB Atlas | Développé avec Streamlit + Python</p>
</div>
""", unsafe_allow_html=True)
