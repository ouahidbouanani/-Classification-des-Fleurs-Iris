"""
Utilitaires Machine Learning pour Iris
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

class IrisMLHelper:
    """Assistant ML pour classification Iris"""
    
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.label_map = {'setosa': 0, 'versicolor': 1, 'virginica': 2}
        self.inv_label_map = {v: k for k, v in self.label_map.items()}
    
    def prepare_data(self, df, test_size=0.2):
        """Prépare les données pour ML"""
        X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']].values
        y = df['species'].map(self.label_map).values
        return train_test_split(X, y, test_size=test_size, random_state=42, stratify=y)
    
    def train_all_models(self, X_train, y_train):
        """Entraîne tous les modèles"""
        self.models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Decision Tree': DecisionTreeClassifier(random_state=42),
            'k-NN': KNeighborsClassifier(n_neighbors=5),
            'SVM': SVC(kernel='rbf', probability=True, random_state=42),
            'Logistic Regression': LogisticRegression(max_iter=200, random_state=42)
        }
        
        print("\n🔄 Entraînement des modèles...")
        for name, model in self.models.items():
            model.fit(X_train, y_train)
            print(f"  ✓ {name}")
    
    def evaluate_models(self, X_test, y_test):
        """Évalue tous les modèles"""
        results = []
        best_acc = 0
        
        for name, model in self.models.items():
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            results.append({'Model': name, 'Accuracy': acc})
            
            if acc > best_acc:
                best_acc = acc
                self.best_model = model
                self.best_model_name = name
        
        return sorted(results, key=lambda x: x['Accuracy'], reverse=True)
    
    def get_predictions(self, X, df):
        """Génère les prédictions pour MongoDB"""
        y_pred = self.best_model.predict(X)
        proba = self.best_model.predict_proba(X)
        
        predictions = []
        for idx, (pred, prob) in enumerate(zip(y_pred, proba)):
            predictions.append({
                'id': f'IR{idx:03d}',
                'prediction': self.inv_label_map[pred],
                'confidence': float(np.max(prob)),
                'model': self.best_model_name
            })
        
        return predictions
    
    def save_model(self, filepath):
        """Sauvegarde le meilleur modèle"""
        joblib.dump({
            'model': self.best_model,
            'name': self.best_model_name,
            'label_map': self.label_map
        }, filepath)
