"""
PARTIES 1 & 2 : Analyse Statistique Descriptive et Visualisation
Projet Classification des Fleurs Iris
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils.data_loader import load_iris_data

# Configuration
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
OUTPUT_DIR = 'outputs/exploratory'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def partie1_analyse_descriptive(df):
    """PARTIE 1 : Analyse statistique descriptive"""
    print("\n" + "="*80)
    print("PARTIE 1 : ANALYSE STATISTIQUE DESCRIPTIVE")
    print("="*80)
    
    # 1. Exploration du dataset
    print("\n📊 1. EXPLORATION DU DATASET")
    print("-"*80)
    print(f"Nombre d'observations : {len(df)}")
    print(f"Nombre de variables : {len(df.columns)}")
    print(f"\nTypes de variables :")
    print(df.dtypes)
    print(f"\nValeurs manquantes :")
    print(df.isnull().sum())
    print(f"\nAperçu des données :")
    print(df.head(10))
    
    # 2. Statistiques descriptives
    print("\n📈 2. STATISTIQUES DESCRIPTIVES")
    print("-"*80)
    feature_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    
    print("\nMoyenne, Médiane, Min, Max, Variance :")
    stats = df[feature_cols].describe()
    stats.loc['variance'] = df[feature_cols].var()
    print(stats)
    
    # 3. Comptage par espèce
    print("\n🌸 3. COMPTAGE PAR ESPÈCE")
    print("-"*80)
    species_count = df['species'].value_counts()
    print(species_count)
    print(f"\nProportions :")
    print(df['species'].value_counts(normalize=True))
    
    # 4. Variables discriminantes
    print("\n🔍 4. VARIABLES DISCRIMINANTES")
    print("-"*80)
    print("\nMoyennes par espèce :")
    print(df.groupby('species')[feature_cols].mean())
    
    # Pouvoir discriminant
    print("\n📊 Pouvoir discriminant (variance inter/intra) :")
    for col in feature_cols:
        between_var = df.groupby('species')[col].mean().var()
        within_var = df.groupby('species')[col].var().mean()
        ratio = between_var / within_var if within_var > 0 else 0
        print(f"  • {col}: {ratio:.4f}")
    
    # RÉPONSES AUX QUESTIONS
    print("\n" + "="*80)
    print("RÉPONSES AUX QUESTIONS - PARTIE 1")
    print("="*80)
    print("\n1. Espèces surreprésentées ?")
    print("   → NON, les 3 espèces sont parfaitement équilibrées (50 observations chacune)")
    
    print("\n2. Différences de taille entre espèces ?")
    setosa_petal = df[df['species']=='setosa']['petal_length'].mean()
    virginica_petal = df[df['species']=='virginica']['petal_length'].mean()
    print(f"   → OUI, différences marquées :")
    print(f"     Pétales Setosa: {setosa_petal:.2f} cm")
    print(f"     Pétales Virginica: {virginica_petal:.2f} cm")
    print(f"     Différence: {virginica_petal-setosa_petal:.2f} cm")
    
    print("\n3. Pétales ou sépales plus discriminants ?")
    print("   → Les PÉTALES sont beaucoup plus discriminants")
    print("     (petal_length et petal_width ont les ratios les plus élevés)")

def partie2_visualisation(df):
    """PARTIE 2 : Visualisation des données"""
    print("\n" + "="*80)
    print("PARTIE 2 : VISUALISATION DES DONNÉES")
    print("="*80)
    
    feature_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    
    # 1. Distribution des variables - Histogrammes
    print("\n📊 1. Génération des HISTOGRAMMES...")
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Histogrammes des Variables par Espèce', fontsize=16, fontweight='bold')
    
    for idx, col in enumerate(feature_cols):
        ax = axes[idx//2, idx%2]
        for species in df['species'].unique():
            data = df[df['species']==species][col]
            ax.hist(data, alpha=0.6, label=species, bins=15)
        ax.set_xlabel(col)
        ax.set_ylabel('Fréquence')
        ax.set_title(f'Distribution de {col}')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/1_histogrammes.png', dpi=300)
    print(f"  ✓ Sauvegardé: {OUTPUT_DIR}/1_histogrammes.png")
    plt.close()
    
    # 2. Boxplots
    print("\n📦 2. Génération des BOXPLOTS...")
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Boxplots par Espèce', fontsize=16, fontweight='bold')
    
    for idx, col in enumerate(feature_cols):
        ax = axes[idx//2, idx%2]
        df.boxplot(column=col, by='species', ax=ax)
        ax.set_xlabel('Espèce')
        ax.set_ylabel(col)
        ax.set_title(f'Boxplot de {col}')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/2_boxplots.png', dpi=300)
    print(f"  ✓ Sauvegardé: {OUTPUT_DIR}/2_boxplots.png")
    plt.close()
    
    # 3. Courbes de densité
    print("\n📉 3. Génération des COURBES DE DENSITÉ...")
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Courbes de Densité', fontsize=16, fontweight='bold')
    
    for idx, col in enumerate(feature_cols):
        ax = axes[idx//2, idx%2]
        for species in df['species'].unique():
            data = df[df['species']==species][col]
            data.plot(kind='density', ax=ax, label=species, alpha=0.7)
        ax.set_xlabel(col)
        ax.set_ylabel('Densité')
        ax.set_title(f'Densité de {col}')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/3_densite.png', dpi=300)
    print(f"  ✓ Sauvegardé: {OUTPUT_DIR}/3_densite.png")
    plt.close()
    
    # 4. Scatter plots - Pétales
    print("\n🔍 4. Génération des SCATTER PLOTS...")
    plt.figure(figsize=(10, 8))
    for species in df['species'].unique():
        data = df[df['species']==species]
        plt.scatter(data['petal_length'], data['petal_width'], 
                   label=species, alpha=0.7, s=100, edgecolors='black', linewidth=0.5)
    plt.xlabel('Longueur des Pétales (cm)', fontsize=12)
    plt.ylabel('Largeur des Pétales (cm)', fontsize=12)
    plt.title('Scatter Plot : Pétales', fontsize=14, fontweight='bold')
    plt.legend(title='Espèce')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/4_scatter_petales.png', dpi=300)
    print(f"  ✓ Sauvegardé: {OUTPUT_DIR}/4_scatter_petales.png")
    plt.close()
    
    # Scatter plots - Sépales
    plt.figure(figsize=(10, 8))
    for species in df['species'].unique():
        data = df[df['species']==species]
        plt.scatter(data['sepal_length'], data['sepal_width'], 
                   label=species, alpha=0.7, s=100, edgecolors='black', linewidth=0.5)
    plt.xlabel('Longueur des Sépales (cm)', fontsize=12)
    plt.ylabel('Largeur des Sépales (cm)', fontsize=12)
    plt.title('Scatter Plot : Sépales', fontsize=14, fontweight='bold')
    plt.legend(title='Espèce')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/5_scatter_sepales.png', dpi=300)
    print(f"  ✓ Sauvegardé: {OUTPUT_DIR}/5_scatter_sepales.png")
    plt.close()
    
    # 5. Matrice de corrélation
    print("\n📈 5. Génération de la MATRICE DE CORRÉLATION...")
    corr_matrix = df[feature_cols].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, linewidths=1, fmt='.3f', vmin=-1, vmax=1)
    plt.title('Matrice de Corrélation', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/6_correlation.png', dpi=300)
    print(f"  ✓ Sauvegardé: {OUTPUT_DIR}/6_correlation.png")
    plt.close()
    
    # Pairplot
    print("\n🎨 6. Génération du PAIRPLOT...")
    pairplot = sns.pairplot(df, hue='species', height=2.5, diag_kind='kde',
                            plot_kws={'alpha':0.6, 's':60, 'edgecolor':'k'})
    pairplot.fig.suptitle('Pairplot : Relations entre Variables', 
                          fontsize=16, fontweight='bold', y=1.01)
    plt.savefig(f'{OUTPUT_DIR}/7_pairplot.png', dpi=300)
    print(f"  ✓ Sauvegardé: {OUTPUT_DIR}/7_pairplot.png")
    plt.close()
    
    # RÉPONSES AUX QUESTIONS
    print("\n" + "="*80)
    print("RÉPONSES AUX QUESTIONS - PARTIE 2")
    print("="*80)
    print("\n1. Variables fortement corrélées ?")
    print("   → petal_length et petal_width (r ≈ 0.96)")
    print("   → petal_length et sepal_length (r ≈ 0.87)")
    
    print("\n2. Biais visuels ?")
    print("   → NON, pas de biais évident")
    print("   → Distribution équilibrée")
    print("   → Pas de valeurs aberrantes majeures")
    
    print("\n3. Observations pour distinguer les espèces ?")
    print("   → Setosa est très facilement séparable (pétales petits)")
    print("   → Versicolor et Virginica se chevauchent légèrement")
    print("   → Les dimensions des PÉTALES sont les plus discriminantes")

def main():
    """Fonction principale"""
    print("\n" + "🌸"*40)
    print("PARTIES 1 & 2 : ANALYSE ET VISUALISATION DES FLEURS IRIS")
    print("🌸"*40)
    
    # Charger les données
    df = load_iris_data(source='auto')
    print(f"✅ Dataset chargé : {len(df)} observations")
    
    # Partie 1
    partie1_analyse_descriptive(df)
    
    # Partie 2  
    partie2_visualisation(df)
    
    print("\n" + "="*80)
    print("✅ PARTIES 1 & 2 TERMINÉES")
    print("="*80)
    print(f"\n📁 Visualisations sauvegardées dans : {OUTPUT_DIR}/")
    print("\n📋 Prochaine étape : python src/partie3_regression.py")

if __name__ == "__main__":
    main()
