import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

#A faire plus tard : vérifier que toutes les variables ne sont pas à None.
#Si elles sont à None, alors on renvoie une erreur.

try:
    connection = psycopg.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)
    print("[INFO] Connexion à PostgreSQL établie.")
except Exception as e:
    print("Erreur : ", e)
    raise

def get_connection():
    return connection