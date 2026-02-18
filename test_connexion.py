"""Test rapide de connexion à MongoDB Atlas"""
import sys
sys.path.append('src')

from utils.mongo_helper import MongoHelper

print("🔌 Test de connexion à MongoDB Atlas...")
try:
    mongo = MongoHelper()
    
    # Test: lister les bases de données
    print("✅ Connexion réussie!")
    print(f"\n📋 Bases de données disponibles:")
    for db_name in mongo.client.list_database_names():
        print(f"  • {db_name}")
    
    # Test: vérifier la base iris_database
    count = mongo.collection.count_documents({})
    print(f"\n📊 Collection 'iris_flowers' dans 'iris_database': {count} documents")
    
    if count == 0:
        print("\n💡 La collection est vide. Pour insérer les données, exécutez:")
        print("   python src/partie4_classification_mongodb.py")
    else:
        # Afficher un exemple de document
        sample = mongo.collection.find_one()
        print(f"\n📄 Exemple de document:")
        for key, value in sample.items():
            if key != '_id':
                print(f"  • {key}: {value}")
    
    mongo.close()
    print("\n✅ Test terminé avec succès!")
    
except Exception as e:
    print(f"\n❌ Erreur de connexion: {e}")
    print("\n💡 Vérifiez:")
    print("   1. Votre URI de connexion dans src/utils/mongo_helper.py")
    print("   2. Que votre IP est autorisée dans MongoDB Atlas (Network Access)")
    print("   3. Que le module 'dnspython' est installé: pip install dnspython")
