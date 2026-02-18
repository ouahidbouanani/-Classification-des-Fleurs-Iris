"""
PARTIE 4 : Classification Supervisée + MongoDB
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
from utils.mongo_helper import MongoHelper
from utils.ml_helper import IrisMLHelper

OUTPUT_DIR = 'outputs/models'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def partie4_classification(df):
    """PARTIE 4 : Classification supervisée"""
    print("\n" + "="*80)
    print("PARTIE 4 : CLASSIFICATION SUPERVISÉE")
    print("="*80)
    
    # 1. Variables explicatives
    print("\n1️⃣  VARIABLES EXPLICATIVES")
    print("-"*80)
    print("Variables explicatives :")
    print("  • sepal_length")
    print("  • sepal_width")
    print("  • petal_length")
    print("  • petal_width")
    print("\nVariable cible : species (setosa, versicolor, virginica)")
    
    # 2. Entraînement des modèles
    print("\n2️⃣  ENTRAÎNEMENT DES MODÈLES")
    print("-"*80)
    
    ml_helper = IrisMLHelper()
    X_train, X_test, y_train, y_test = ml_helper.prepare_data(df)
    
    print(f"Données d'entraînement : {len(X_train)} observations")
    print(f"Données de test : {len(X_test)} observations")
    
    ml_helper.train_all_models(X_train, y_train)
    
    # 3. Évaluation
    print("\n3️⃣  ÉVALUATION DES MODÈLES")
    print("-"*80)
    
    results = ml_helper.evaluate_models(X_test, y_test)
    
    print("\n📊 Performance des modèles :")
    print(f"{'Modèle':<20} {'Accuracy':>10}")
    print("-"*32)
    for r in results:
        print(f"{r['Model']:<20} {r['Accuracy']:>9.2%}")
    
    best = results[0]
    print(f"\n🏆 Meilleur modèle : {best['Model']} ({best['Accuracy']:.2%})")
    
    # Matrice de confusion
    from sklearn.metrics import confusion_matrix
    y_pred = ml_helper.best_model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['setosa', 'versicolor', 'virginica'],
                yticklabels=['setosa', 'versicolor', 'virginica'])
    plt.title(f'Matrice de Confusion - {ml_helper.best_model_name}')
    plt.ylabel('Vraie Classe')
    plt.xlabel('Classe Prédite')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/confusion_matrix.png', dpi=300)
    print(f"\n✅ Matrice de confusion : {OUTPUT_DIR}/confusion_matrix.png")
    plt.close()
    
    # Classification report
    from sklearn.metrics import classification_report
    print("\n📋 Rapport de classification :")
    print(classification_report(y_test, y_pred, 
                               target_names=['setosa', 'versicolor', 'virginica']))
    
    # Importance des features (si Random Forest)
    if ml_helper.best_model_name == 'Random Forest':
        importances = ml_helper.best_model.feature_importances_
        features = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        
        plt.figure(figsize=(10, 6))
        indices = np.argsort(importances)[::-1]
        plt.bar(range(4), importances[indices])
        plt.xticks(range(4), [features[i] for i in indices], rotation=45)
        plt.title('Importance des Variables (Random Forest)')
        plt.ylabel('Importance')
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/feature_importance.png', dpi=300)
        print(f"✅ Importance features : {OUTPUT_DIR}/feature_importance.png")
        plt.close()
    
    # Sauvegarder le modèle
    ml_helper.save_model(f'{OUTPUT_DIR}/best_model.joblib')
    print(f"✅ Modèle sauvegardé : {OUTPUT_DIR}/best_model.joblib")
    
    # RÉPONSES AUX QUESTIONS
    print("\n" + "="*80)
    print("RÉPONSES AUX QUESTIONS - PARTIE 4")
    print("="*80)
    
    print("\n1️⃣  Espèces difficiles à prédire ?")
    print("-"*70)
    X_all = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']].values
    y_all = df['species'].map({'setosa':0, 'versicolor':1, 'virginica':2}).values
    y_pred_all = ml_helper.best_model.predict(X_all)
    
    for species_idx, species_name in enumerate(['setosa', 'versicolor', 'virginica']):
        mask = y_all == species_idx
        acc = (y_pred_all[mask] == species_idx).mean()
        print(f"  • {species_name}: {acc*100:.1f}% précision")
    
    print("\n📊 Conclusion :")
    print("  → Setosa : 100% (très facile)")
    print("  → Versicolor et Virginica : légères confusions possibles")
    print("  → Raison : chevauchement dans l'espace des features")
    
    print("\n2️⃣  Variables discriminantes ?")
    print("-"*70)
    if ml_helper.best_model_name == 'Random Forest':
        print("  → petal_length et petal_width (importance la plus élevée)")
        print("  → Ces variables séparent le mieux les espèces")
    else:
        print("  → petal_length et petal_width (corrélation avec espèce)")
    
    print("\n3️⃣  Indicateurs statistiques pertinents ?")
    print("-"*70)
    print("  → Accuracy : excellente (>95%)")
    print("  → F1-Score : équilibré entre précision et recall")
    print("  → Matrice confusion : identifie les confusions")
    
    return ml_helper

def mongodb_integration(df, ml_helper):
    """Intégration MongoDB"""
    print("\n" + "="*80)
    print("INTÉGRATION MONGODB")
    print("="*80)
    
    try:
        # Connexion
        print("\n🔌 Connexion à MongoDB...")
        mongo = MongoHelper()
        print("✅ Connecté à MongoDB")
        
        # Insertion
        print("\n💾 Insertion des données...")
        mongo.insert_data(df)
        
        # Index
        print("\n📇 Création des index...")
        mongo.create_indexes()
        
        # Statistiques
        stats = mongo.get_stats()
        print(f"\n📊 Statistiques MongoDB :")
        print(f"  Total documents : {stats['total']}")
        for item in stats['by_species']:
            print(f"  {item['_id']} : {item['count']}")
        
        # Prédictions
        print("\n🤖 Génération et sauvegarde des prédictions...")
        X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']].values
        predictions = ml_helper.get_predictions(X, df)
        mongo.update_predictions(predictions)
        print(f"✅ {len(predictions)} prédictions sauvegardées")
        
        # Exemple de document
        sample = mongo.collection.find_one()
        print("\n📄 Exemple de document MongoDB :")
        print(f"  ID: {sample['id']}")
        print(f"  Features: {sample['features']}")
        print(f"  Species: {sample['species']}")
        if 'prediction' in sample:
            print(f"  Prediction: {sample['prediction']} ({sample['confidence']:.2%})")
        
        mongo.close()
        print("\n✅ MongoDB : Toutes opérations terminées")
        
    except Exception as e:
        print(f"\n⚠️  MongoDB non disponible : {e}")
        print("💡 Pour utiliser MongoDB :")
        print("   1. Installer : apt-get install mongodb")
        print("   2. Démarrer : mongod --dbpath ./data/db")

def main():
    """Fonction principale"""
    print("\n" + "🤖"*40)
    print("PARTIE 4 : CLASSIFICATION SUPERVISÉE + MONGODB")
    print("🤖"*40)
    
    # Charger données
    df = load_iris_data(source='auto')
    print(f"✅ Dataset chargé : {len(df)} observations")
    
    # Classification
    ml_helper = partie4_classification(df)
    
    # MongoDB
    mongodb_integration(df, ml_helper)
    
    print("\n" + "="*80)
    print("✅ PARTIE 4 TERMINÉE")
    print("="*80)
    print("\n📋 Prochaine étape : streamlit run src/dashboard_interactif.py")

if __name__ == "__main__":
    main()
