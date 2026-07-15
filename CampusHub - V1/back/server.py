"""
Projet: CampusHub
Fichier: server.py
Description: Organisation des routes et démarrage de FastAPI
Auteur: G. Eraste
Date: 7 Juillet 2026
"""

#=== IMPORTS =================================
from fastapi import FastAPI

from database import get_connection
from dependencies import get_current_user

from utilisateurs import router as usr_router
from matieres import router as mat_router
from taches import router as tac_router
#=============================================


app = FastAPI(title="CampusHub API", description="API de gestion des tâches et matières étudiantes.", version="1.0.0")

app.include_router(usr_router)
app.include_router(mat_router)
app.include_router(tac_router)

@app.get("/")
def accueil():
    return {"message": "API CampusHub opérationnelle."}
