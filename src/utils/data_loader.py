"""
Chargeur de données Iris - Support UCI ML Repo, Kaggle et sklearn
Python 3.13.2
"""
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def load_iris_data(source='auto'):
    """
    Charge les données Iris depuis différentes sources
    
    Args:
        source: 'auto', 'uci', 'kaggle', ou 'sklearn'
    
    Returns:
        DataFrame avec colonnes: sepal_length, sepal_width, petal_length, petal_width, species
    """
    print(f"\n📥 Chargement des données Iris (source: {source})...")
    
    if source == 'uci':
        try:
            from ucimlrepo import fetch_ucirepo
            iris = fetch_ucirepo(id=53)
            X = iris.data.features
            y = iris.data.targets
            df = pd.concat([X, y], axis=1)
            df.columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
            df['species'] = df['species'].str.replace('Iris-', '', regex=False).str.lower()
            print("✅ Données chargées depuis UCI ML Repository")
            return df
        except:
            print("⚠️  UCI non disponible, utilisation de sklearn")
            return load_iris_data(source='sklearn')
    
    elif source == 'kaggle':
        try:
            import kagglehub
            path = kagglehub.dataset_download("uciml/iris")
            import glob
            csv_file = glob.glob(f"{path}/**/*.csv", recursive=True)[0]
            df = pd.read_csv(csv_file)
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            if 'id' in df.columns:
                df = df.drop('id', axis=1)
            print("✅ Données chargées depuis Kaggle")
            return df
        except:
            print("⚠️  Kaggle non disponible, utilisation de sklearn")
            return load_iris_data(source='sklearn')
    
    elif source == 'sklearn' or source == 'auto':
        from sklearn.datasets import load_iris
        iris = load_iris()
        df = pd.DataFrame(iris.data, columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])
        df['species'] = pd.Categorical.from_codes(iris.target, ['setosa', 'versicolor', 'virginica'])
        print("✅ Données chargées depuis sklearn")
        return df
    
    else:
        raise ValueError(f"Source inconnue: {source}")
