# app.py à la racine du projet
import sys
import os

# Ajouter le dossier src au PATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importer tout depuis dashboard_interactif
from dashboard_interactif import *