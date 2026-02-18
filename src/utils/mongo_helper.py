"""
Utilitaires MongoDB pour le projet Iris
"""
from pymongo import MongoClient, ASCENDING
from datetime import datetime
import pandas as pd

class MongoHelper:
    """Gestionnaire MongoDB pour Iris"""
    
    def __init__(self, uri="mongodb+srv://bouananiouahid_db_user:3C1JqdRD9hT76BgH@cluster0.qe1ldir.mongodb.net/?appName=Cluster0", db_name="iris_database", collection_name="iris_flowers"):
        """
        Initialise la connexion MongoDB avec une URI (par défaut, celle fournie par l'utilisateur).
        db_name et collection_name sont personnalisables si besoin.
        """
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
    
    def insert_data(self, df):
        """Insère les données dans MongoDB"""
        self.collection.drop()  # Nettoyer
        
        documents = []
        for idx, row in df.iterrows():
            doc = {
                "id": f"IR{idx:03d}",
                "features": {
                    "sepal_length": float(row['sepal_length']),
                    "sepal_width": float(row['sepal_width']),
                    "petal_length": float(row['petal_length']),
                    "petal_width": float(row['petal_width'])
                },
                "species": row['species'],
                "created_at": datetime.now()
            }
            documents.append(doc)
        
        self.collection.insert_many(documents)
        print(f"✅ {len(documents)} documents insérés dans MongoDB")
        return len(documents)
    
    def create_indexes(self):
        """Crée les index pour optimisation"""
        self.collection.create_index([("species", ASCENDING)], name="idx_species")
        self.collection.create_index([
            ("features.petal_length", ASCENDING),
            ("features.petal_width", ASCENDING)
        ], name="idx_petal_features")
        print("✅ Index MongoDB créés")
    
    def get_stats(self):
        """Retourne les statistiques de la collection"""
        return {
            "total": self.collection.count_documents({}),
            "by_species": list(self.collection.aggregate([
                {"$group": {"_id": "$species", "count": {"$sum": 1}}}
            ]))
        }
    
    def update_predictions(self, predictions_list):
        """Met à jour avec les prédictions"""
        for pred in predictions_list:
            self.collection.update_one(
                {"id": pred['id']},
                {"$set": {
                    "prediction": pred['prediction'],
                    "confidence": pred['confidence'],
                    "model": pred['model']
                }}
            )
    
    def close(self):
        self.client.close()
