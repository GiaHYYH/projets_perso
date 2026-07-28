"""
Projet: CampusHub
Fichier: dashboard.py
Description: Fichier contenant toutes les routes pour le tableau de bord
Auteur: G. Eraste
Date: 15 Juillet 2026
"""

#=== IMPORTS =============================
from fastapi import APIRouter, Depends

from database import get_connection
from dependencies import get_current_user
from models import Dashboard, DashboardMatiere, DashboardRetard, DashboardUrgente
#=========================================

router = APIRouter()

@router.get("/dashboard", response_model=Dashboard)
def lire_dashboard(usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*), COUNT(*) FILTER (WHERE tac_status = 'A'), COUNT(*) FILTER (WHERE tac_status = 'E'), COUNT(*) FILTER (WHERE tac_status = 'T'), COALESCE(SUM(tac_duree), 0), COUNT(*) FILTER (WHERE tac_priorite = 'H' AND tac_status <> 'T') FROM t_tache_tac WHERE usr_mail = %s;", (usr_mail,))
            resultat = cursor.fetchone()

            return {"nombre_total_taches": resultat[0], "taches_a_faire": resultat[1], "taches_en_cours": resultat[2], "taches_terminees": resultat[3], "temps_total_estime": resultat[4], "taches_urgentes": resultat[5]}
        
    
@router.get("/dashboard/matieres", response_model=list[DashboardMatiere])
def dashboard_matieres(usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT m.mat_id, m.mat_nom, COUNT(t.tac_id), COALESCE(SUM(t.tac_duree), 0) FROM t_matiere_mat m LEFT JOIN t_lien_matiere_tache_lmt l USING(mat_id) LEFT JOIN t_tache_tac t USING(tac_id) WHERE m.usr_mail = %s GROUP BY m.mat_id, m.mat_nom ORDER BY m.mat_nom;", (usr_mail,))

            resultats = cursor.fetchall()
            liste = []

            for resultat in resultats:
                liste.append({"mat_id": resultat[0], "mat_nom": resultat[1], "nombres_taches": resultat[2], "temps_total_estime": resultat[3]})

            return liste


@router.get("/dashboard/retards", response_model=list[DashboardRetard])
def lire_taches_en_retard(usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT tac_id, tac_nom, tac_date_limite, tac_priorite, CURRENT_DATE - tac_date_limite AS jours_retard FROM t_tache_tac WHERE usr_mail = %s AND tac_status <> 'T' AND tac_date_limite < CURRENT_DATE ORDER BY jours_retard DESC, tac_priorite DESC;", (usr_mail,))
            resultats = cursor.fetchall()
            
            liste = []

            for resultat in resultats:
                liste.append({"tac_id": resultat[0], "tac_nom": resultat[1], "tac_date_limite": resultat[2], "tac_priorite": resultat[3], "jours_retard": resultat[4]})

            return liste 

@router.get("/dashboard/urgentes", response_model=list[DashboardUrgente])
def lire_taches_urgentes(usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT tac_id, tac_nom, tac_date_limite, tac_priorite FROM t_tache_tac WHERE usr_mail = %s AND tac_status <> 'T' AND tac_priorite = 'H' ORDER BY tac_date_limite ASC NULLS LAST;", (usr_mail,))
            resultats = cursor.fetchall()

            liste = []

            for resultat in resultats:
                liste.append({"tac_id": resultat[0], "tac_nom": resultat[1], "tac_date_limite": resultat[2], "tac_priorite": resultat[3]})

            return liste