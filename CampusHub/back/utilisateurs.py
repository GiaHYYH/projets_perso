"""
Projet: CampusHub
Fichier: utilisateurs.py
Description: Organisation du CRUD pour la table SQL des utilisateurs
Auteur: G. Eraste
Date: 9 Juillet 2026
"""

#=== IMPORTS ========================================
from fastapi import APIRouter, status, HTTPException, Depends
from passlib.hash import bcrypt

from database import get_connection
from models import UtilisateurCreation, UtilisateurConnexion, UtilisateurModification, Utilisateur
from auth import create_jwt
from dependencies import get_current_user
#====================================================

router = APIRouter()

@router.post("/utilisateurs", status_code=status.HTTP_201_CREATED)
def creer_utilisateur(utilisateur: UtilisateurCreation):

    with get_connection() as conn:

        with conn.cursor() as cursor:
            cursor.execute("SELECT usr_mail FROM t_utilisateur_usr WHERE usr_mail = %s;", (utilisateur.usr_mail, ))
            result = cursor.fetchone()

            if result is not None:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cette adresse e-mail est déjà utilisée.")

            
            hashed_password = bcrypt.hash(utilisateur.usr_mdp)

            cursor.execute("INSERT INTO t_utilisateur_usr (usr_mail, usr_mdp, usr_nom, usr_prenom, usr_niveau, usr_formation) VALUES (%s, %s, %s, %s, %s, %s);", (utilisateur.usr_mail, hashed_password, utilisateur.usr_nom, utilisateur.usr_prenom, utilisateur.usr_niveau, utilisateur.usr_formation))
            conn.commit()

            return {"message": "L'utilisateur a bien été créé.", "usr_mail": utilisateur.usr_mail}
    

@router.post("/connexion")
def connecter_utilisateur(utilisateur: UtilisateurConnexion):
    with get_connection() as conn:

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


@router.get("/profil", response_model=Utilisateur)
def lire_profil(usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute("SELECT usr_mail, usr_nom, usr_prenom, usr_niveau, usr_formation FROM t_utilisateur_usr WHERE usr_mail = %s;", (usr_mail,))
            resultat = cursor.fetchone()

            if resultat is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable.")
            
            return {"usr_mail": resultat[0], "usr_nom": resultat[1], "usr_prenom": resultat[2], "usr_niveau": resultat[3], "usr_formation": resultat[4]}
        

@router.put("/profil")
def modifier_profil(modification: UtilisateurModification, usr_mail: str = Depends(get_current_user)):

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE t_utilisateur_usr SET usr_nom = %s, usr_prenom = %s, usr_niveau = %s, usr_formation = %s WHERE usr_mail = %s;", (modification.usr_nom, modification.usr_prenom, modification.usr_niveau, modification.usr_formation, usr_mail))

            if cursor.rowcount == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable.")

            conn.commit()

            return {"message": "Le profil a bien été modifié."}


@router.delete("/profil")
def supprimer_compte(usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM t_utilisateur_usr WHERE usr_mail = %s;", (usr_mail,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable.")

            conn.commit()

            return {"message": "Votre compte a été supprimé."}