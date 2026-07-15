"""
Projet: CampusHub
Fichier: dependencies.py
Description: Pont entre JWT et routes protégées
Auteur: G. Eraste
Date: 13 Juillet 2026
"""

#=== IMPORTS ========================================================
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth import verify_jwt
#====================================================================

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Retourne l'utilisateur actuel"""
    token = credentials.credentials

    current_user = verify_jwt(token)

    return current_user