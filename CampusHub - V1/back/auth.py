"""
Projet: CampusHub
Fichier: models.py
Description: Authentification d'un compte utilisateur
Auteur: G. Eraste
Date: 13 Juillet 2026
"""

#=== IMPORTS =======================================
import os
import jwt

from fastapi import status, HTTPException
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
#===================================================

load_dotenv()

jwt_secret = os.getenv("JWT_SECRET")
jwt_algorithm = os.getenv("JWT_ALGORITHM")

if jwt_secret is None or jwt_algorithm is None:
    raise RuntimeError("Configuration JWT absente.")


def create_jwt(usr_mail: str):
    """Création du token JWT"""
    now = datetime.now(timezone.utc)
    payload = {"sub": usr_mail, "iat": now, "exp": now + timedelta(minutes=30)}
    
    return jwt.encode(payload, jwt_secret, algorithm=jwt_algorithm)


def verify_jwt(token: str) -> str:
    """Vérification du token JWT"""
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm])
        
        usr_mail = payload.get("sub")

        if usr_mail is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide.")
        
        return usr_mail
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide.")
