"""
Projet: CampusHub
Fichier: taches.py
Description: Organisation du CRUD pour la table SQL des tâches
Auteur: G. Eraste
Date: 9 Juillet 2026
"""

#=== IMPORTS =================================================================================
from fastapi import APIRouter, status, HTTPException, Depends

from models import TacheCreation, Tache, TacheModification, TacheStatutModification, Matiere
from database import get_connection
from dependencies import get_current_user
#==============================================================================================

router = APIRouter()


@router.post("/taches", status_code=status.HTTP_201_CREATED)
def creer_tache(tache: TacheCreation, usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
    
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO t_tache_tac (tac_nom, tac_duree, tac_status, usr_mail) VALUES (%s, %s, %s, %s) RETURNING tac_id;", (tache.tac_nom, tache.tac_duree, "A", usr_mail))
            result = cursor.fetchone()
            if result is None:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="La création de la tâche a échoué.")
            tac_id = result[0]
            conn.commit()
            return {"message": "La tâche a bien été créée.", "tac_id": tac_id}
        

@router.get("/taches", response_model = list[Tache])
def lire_taches(usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:

        with conn.cursor() as cursor:
            cursor.execute("SELECT tac_id, tac_nom, tac_duree, tac_status FROM t_tache_tac WHERE usr_mail = %s;", (usr_mail,))
            resultats = cursor.fetchall()

            liste = []

            for resultat in resultats:
                liste.append({"tac_id": resultat[0], "tac_nom": resultat[1], "tac_duree": resultat[2], "tac_status": resultat[3]})

        return liste


@router.patch("/taches/{tac_id}/statut")
def modifier_statut_tache(tac_id: int, modification: TacheStatutModification, usr_mail: str = Depends(get_current_user)):

    with get_connection() as conn:

        with conn.cursor() as cursor:
            cursor.execute("UPDATE t_tache_tac SET tac_status = %s WHERE tac_id = %s AND usr_mail = %s;", (modification.tac_status, tac_id, usr_mail))

            if cursor.rowcount == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cette tâche est introuvable.")
            
            conn.commit()

            return {"message" : "Le statut de la tâche a été modifié."}
    

@router.put("/taches/{tac_id}")
def modifier_tache(tac_id: int, modification: TacheModification, usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:

        with conn.cursor() as cursor:
            cursor.execute("UPDATE t_tache_tac SET tac_nom = %s, tac_duree = %s WHERE tac_id = %s AND usr_mail = %s;", (modification.tac_nom, modification.tac_duree, tac_id, usr_mail))

            if cursor.rowcount == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cette tâche est introuvable.")
            
            conn.commit()

            return {"message": "La tâche à bien été modifiée."}
    

@router.delete("/taches/{tac_id}")
def supprimer_tache(tac_id: int, usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:

        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM t_tache_tac WHERE tac_id = %s AND usr_mail = %s;", (tac_id, usr_mail))

            if cursor.rowcount == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cette tâche est introuvable.")
            
            conn.commit()
            return {"message": "La tâche a bien été supprimée."}
    

@router.post("/taches/{tac_id}/matieres/{mat_id}")
def lier_tache_matiere(tac_id: int, mat_id: int, usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
    
        with conn.cursor() as cursor:
            cursor.execute("SELECT tac_id FROM t_tache_tac WHERE tac_id = %s AND usr_mail = %s;", (tac_id, usr_mail))
            tache = cursor.fetchone()
            if tache is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cette tâche est introuvable.")
                
            cursor.execute("SELECT mat_id FROM t_matiere_mat WHERE mat_id = %s AND usr_mail = %s;", (mat_id, usr_mail))
            matiere = cursor.fetchone()
            if matiere is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cette matière est introuvable.")
            
            cursor.execute("SELECT 1 FROM t_lien_matiere_tache_lmt WHERE mat_id = %s AND tac_id = %s;", (mat_id, tac_id))
            lien = cursor.fetchone()
            if lien is not None:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cette tâche est déjà associée à cette matière.")
                
            cursor.execute("INSERT INTO t_lien_matiere_tache_lmt (mat_id, tac_id) VALUES (%s, %s);", (mat_id, tac_id))
            conn.commit()
            
            return {"message": "La tâche a bien été associée à la matière."}
        

@router.get("/taches/{tac_id}/matieres", response_model=list[Matiere])
def lire_matieres_tache(tac_id: int, usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
    
        with conn.cursor() as cursor:
            cursor.execute("SELECT tac_id FROM t_tache_tac WHERE tac_id = %s AND usr_mail = %s;", (tac_id, usr_mail))
            result = cursor.fetchone()
            if result is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cette tâche est introuvable.")
            
            cursor.execute("SELECT m.mat_id, m.mat_nom, m.mat_couleur FROM t_lien_matiere_tache_lmt l JOIN t_matiere_mat m USING(mat_id) WHERE l.tac_id = %s AND m.usr_mail = %s;", (tac_id, usr_mail))
            resultats = cursor.fetchall()
            
            liste = []
            
            for resultat in resultats:
                liste.append({"mat_id": resultat[0], "mat_nom": resultat[1], "mat_couleur": resultat[2]})
            
            return liste
    

@router.delete("/taches/{tac_id}/matieres/{mat_id}")
def supprimer_lien_tache_matiere(tac_id: int, mat_id: int, usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:

        with conn.cursor() as cursor:
            cursor.execute("SELECT tac_id FROM t_tache_tac WHERE tac_id = %s AND usr_mail = %s;", (tac_id, usr_mail))
            tache = cursor.fetchone()
            if tache is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cette tâche est introuvable.")
                
            cursor.execute("SELECT mat_id FROM t_matiere_mat WHERE mat_id = %s AND usr_mail = %s;", (mat_id, usr_mail))
            matiere = cursor.fetchone()
            if matiere is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cette matière est introuvable.")
            
            cursor.execute("DELETE FROM t_lien_matiere_tache_lmt WHERE tac_id = %s AND mat_id = %s;", (tac_id, mat_id))

            if cursor.rowcount == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ce lien est introuvable.")
            
            conn.commit()
            return {"message": "Le lien entre la tâche et la matière a bien été supprimé."}