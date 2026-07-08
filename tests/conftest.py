import os
import sys

# Les modules de l'application utilisent des chemins relatifs (TIWAP.db,
# helper/sqlite_db_reset.txt, certificate/...) : on se place a la racine du projet.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)
