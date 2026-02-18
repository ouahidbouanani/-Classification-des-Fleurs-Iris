#!/usr/bin/env python3
"""
Script principal pour exécuter TOUTES les parties du projet
Projet Classification des Fleurs Iris
"""
import os
import sys
import subprocess

def run_script(script_path, description):
    """Exécute un script Python"""
    print("\n" + "="*80)
    print(f"▶️  {description}")
    print("="*80)
    
    result = subprocess.run([sys.executable, script_path], capture_output=False)
    
    if result.returncode == 0:
        print(f"\n✅ {description} - TERMINÉ")
        return True
    else:
        print(f"\n❌ {description} - ERREUR")
        return False

def main():
    print("\n" + "🌸"*40)
    print("EXÉCUTION COMPLÈTE DU PROJET IRIS CLASSIFICATION")
    print("🌸"*40)
    
    scripts = [
        ("src/partie1_2_analyse_visualisation.py", "PARTIES 1 & 2 : Analyse et Visualisation"),
        ("src/partie3_regression.py", "PARTIE 3 : Régression Simple et Multiple"),
        ("src/partie4_classification_mongodb.py", "PARTIE 4 : Classification + MongoDB"),
    ]
    
    results = {}
    
    for script, desc in scripts:
        if os.path.exists(script):
            results[desc] = run_script(script, desc)
        else:
            print(f"\n⚠️  Fichier non trouvé : {script}")
            results[desc] = False
    
    # Résumé
    print("\n" + "="*80)
    print("📊 RÉSUMÉ DE L'EXÉCUTION")
    print("="*80)
    
    for desc, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {desc}")
    
    # Dashboard
    print("\n" + "="*80)
    print("🎯 ÉTAPE FINALE : DASHBOARD INTERACTIF")
    print("="*80)
    print("\nPour lancer le dashboard interactif (Partie 4 - Prototype) :")
    print("  streamlit run src/dashboard_interactif.py")
    
    print("\n" + "="*80)
    if all(results.values()):
        print("✅ PROJET COMPLET EXÉCUTÉ AVEC SUCCÈS !")
    else:
        print("⚠️  PROJET EXÉCUTÉ AVEC QUELQUES ERREURS")
    print("="*80)
    
    print("\n📁 Résultats générés dans :")
    print("  • outputs/exploratory/ - Visualisations")
    print("  • outputs/models/ - Modèles ML")
    print("  • outputs/reports/ - Rapports")

if __name__ == "__main__":
    main()
