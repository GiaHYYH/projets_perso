"""
Projet: CampusHub
Fichier: database.py
Description: Gestion des connexions et de erreurs SQL
Auteur: G. Eraste
Date: 8 Juillet 2026
"""

#=== IMPORTS ==================
import os

import psycopg
from dotenv import load_dotenv
#==============================

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

if None in [db_host, db_port, db_name, db_user, db_password]:
    raise RuntimeError("Configuration PostrgreSQL incomplète.")


def get_connection():
    """Retourne une connection"""
    return psycopg.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)