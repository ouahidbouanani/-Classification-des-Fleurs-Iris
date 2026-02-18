"""Vérification des index MongoDB"""
import sys
sys.path.append('src')
from utils.mongo_helper import MongoHelper

mongo = MongoHelper()

print("📇 Index actifs dans MongoDB:")
for idx in mongo.collection.list_indexes():
    print(f"  - {idx['name']}: {idx['key']}")

print(f"\n📊 Documents: {mongo.collection.count_documents({})}")

# Vérifier un document avec prédiction
sample = mongo.collection.find_one({"prediction": {"$exists": True}})
if sample:
    print(f"\n📄 Exemple de document avec prédiction:")
    for k, v in sample.items():
        if k != '_id':
            print(f"  {k}: {v}")

mongo.close()
