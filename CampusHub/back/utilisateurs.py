from fastapi import APIRouter, status, HTTPException
from passlib.hash import bcrypt

from database import get_connection
from models import UtilisateurCreation, UtilisateurConnexion
from auth import create_jwt

router = APIRouter()

@router.post("/utilisateurs", status_code=status.HTTP_201_CREATED)
def creer_utilisateur(utilisateur: UtilisateurCreation):

    conn = get_connection()

    with conn.cursor() as cursor:
        cursor.execute("SELECT usr_mail FROM t_utilisateur_usr WHERE usr_mail = %s;", (utilisateur.usr_mail, ))
        result = cursor.fetchone()

        if result is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cette adresse e-mail est déjà utilisée.")

        
        hashed_password = bcrypt.hash(utilisateur.usr_mdp)

        cursor.execute("INSERT INTO t_utilisateur_usr (usr_mail, usr_mdp, usr_nom, usr_prenom, usr_niveau, usr_formation) VALUES (%s, %s, %s, %s, %s, %s);", (utilisateur.usr_mail, hashed_password, utilisateur.usr_nom, utilisateur.usr_prenom, utilisateur.usr_niveau, utilisateur.usr_formation))
        conn.commit()

        return {"message": "L'utilisateur a bien été créé."}
    

@router.post("/connexion")
def connecter_utilisateur(utilisateur: UtilisateurConnexion):
    conn = get_connection()

    with conn.cursor() as cursor:
        cursor.execute("SELECT usr_mail, usr_mdp FROM t_utilisateur_usr WHERE usr_mail = %s;", (utilisateur.usr_mail, ))
        result = cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Adresse e-mail ou mot de passe incorrect.")

        hash_stocke = result[1]
    
    if bcrypt.verify(utilisateur.usr_mdp, hash_stocke):
        token = create_jwt(utilisateur.usr_mail)
        return {"message": "Connexion réussie.", "access_token": token}

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Adresse e-mail ou mot de passe incorrect.")