"""
Projet: CampusHub
Fichier: matieres.py
Description: Organisation du CRUD pour la table SQL des matières
Auteur: G. Eraste
Date: 9 Juillet 2026
"""

#=== IMPORTS =================================================
from fastapi import APIRouter, status, HTTPException, Depends

from models import MatiereCreation, MatiereModification, Matiere, Tache
from database import get_connection
from dependencies import get_current_user
#=============================================================

router = APIRouter()

@router.post("/matieres", status_code=status.HTTP_201_CREATED)
def creer_matiere(matiere: MatiereCreation, usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
    
        with conn.cursor() as cursor:
            cursor.execute("SELECT mat_id FROM t_matiere_mat WHERE usr_mail = %s AND mat_nom = %s;", (usr_mail, matiere.mat_nom))
            result = cursor.fetchone()

            if result is not None:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cette matière existe déjà pour cet utilisateur.")

            cursor.execute("INSERT INTO t_matiere_mat (mat_nom, mat_couleur, usr_mail) VALUES (%s, %s, %s);", (matiere.mat_nom, matiere.mat_couleur, usr_mail))
            conn.commit()

            return {"message": "La matière a bien été créée."}
    
@router.get("/matieres", response_model = list[Matiere])
def lire_matieres(usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:

        with conn.cursor() as cursor:
            cursor.execute("SELECT mat_id, mat_nom, mat_couleur FROM t_matiere_mat WHERE usr_mail = %s ORDER BY mat_nom;", (usr_mail,))
            resultats = cursor.fetchall()

            liste = []

            for resultat in resultats:
                liste.append({"mat_id": resultat[0], "mat_nom": resultat[1], "mat_couleur": resultat[2]})

        return liste


@router.delete("/matieres/{mat_id}")
def supprimer_matiere(mat_id: int, usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM t_matiere_mat WHERE mat_id = %s AND usr_mail = %s;", (mat_id, usr_mail))

            if cursor.rowcount == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cette matière est introuvable.")
            
            conn.commit()
            return {"message": "La matière a bien été supprimée."}
    

@router.put("/matieres/{mat_id}")
def modifier_matiere(mat_id: int, matiere: MatiereModification, usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:

        with conn.cursor() as cursor:
            cursor.execute("SELECT mat_id FROM t_matiere_mat WHERE usr_mail = %s AND mat_nom = %s AND mat_id <> %s;", (usr_mail, matiere.mat_nom, mat_id))
            result = cursor.fetchone()

            if result is not None:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cette matière existe déjà pour cet utilisateur.")
            
            cursor.execute("UPDATE t_matiere_mat SET mat_nom = %s, mat_couleur = %s WHERE mat_id = %s AND usr_mail = %s;", (matiere.mat_nom, matiere.mat_couleur, mat_id, usr_mail))
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cette matière est introuvable.")
            
            conn.commit()

            return {"message": "La matière a été modifiée."}
    

@router.get("/matieres/{mat_id}/taches", response_model=list[Tache])
def lire_taches_matiere(mat_id: int, usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
    
        with conn.cursor() as cursor:
            cursor.execute("SELECT mat_id FROM t_matiere_mat WHERE mat_id = %s AND usr_mail = %s;", (mat_id, usr_mail))
            result = cursor.fetchone()
            if result is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cette matière est introuvable.")
            
            cursor.execute("SELECT t.tac_id, t.tac_nom, t.tac_duree, t.tac_status FROM t_lien_matiere_tache_lmt l JOIN t_tache_tac t USING(tac_id) WHERE l.mat_id = %s AND t.usr_mail = %s ORDER BY t.tac_nom;", (mat_id, usr_mail))
            resultats = cursor.fetchall()
            
            liste = []
            
            for resultat in resultats:
                liste.append({"tac_id": resultat[0], "tac_nom": resultat[1], "tac_duree": resultat[2], "tac_status": resultat[3]})
            
            return liste