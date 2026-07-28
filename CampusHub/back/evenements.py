from fastapi import APIRouter, Depends, HTTPException, status

from database import get_connection
from dependencies import get_current_user
from models import (Evenement, EvenementCreation, EvenementModification)

router = APIRouter()

@router.post("/evenements", status_code=status.HTTP_201_CREATED)
def creer_evenement(evenement: EvenementCreation, usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO t_evenement_evt (evt_nom, evt_date, evt_heure_debut, evt_heure_fin, evt_type, evt_description, evt_couleur, usr_mail) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING evt_id;", (evenement.evt_nom, evenement.evt_date, evenement.evt_heure_debut, evenement.evt_heure_fin, evenement.evt_type, evenement.evt_description, evenement.evt_couleur, usr_mail))
            evt_id = cursor.fetchone()[0]
            conn.commit()
            return {"message": "L'événement a bien été créé.", "evt_id": evt_id}


@router.get("/evenements", response_model=list[Evenement])
def lire_evenements(usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT evt_id, evt_nom, evt_date, evt_heure_debut, evt_heure_fin, evt_type, evt_description, evt_couleur FROM t_evenement_evt WHERE usr_mail = %s ORDER BY evt_date, evt_heure_debut;", (usr_mail,))
            resultats = cursor.fetchall()

            liste = []

            for resultat in resultats:
                liste.append({"evt_id": resultat[0], "evt_nom": resultat[1], "evt_date": resultat[2], "evt_heure_debut": resultat[3], "evt_heure_fin": resultat[4], "evt_type": resultat[5], "evt_description": resultat[6], "evt_couleur": resultat[7]})

            return liste


@router.put("/evenements/{evt_id}")
def modifier_evenement(evt_id: int, evenement: EvenementModification, usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE t_evenement_evt SET evt_nom = %s, evt_date = %s, evt_heure_debut = %s, evt_heure_fin = %s, evt_type = %s, evt_description = %s, evt_couleur = %s WHERE evt_id = %s AND usr_mail = %s;", (evenement.evt_nom, evenement.evt_date, evenement.evt_heure_debut, evenement.evt_heure_fin, evenement.evt_type, evenement.evt_description, evenement.evt_couleur, evt_id, usr_mail))

            if cursor.rowcount == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cet événement est introuvable.")
            
            conn.commit()

            return {"message": "L'événement a bien été modifié."}


@router.delete("/evenements/{evt_id}")
def supprimer_evenement(evt_id: int, usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM t_evenement_evt WHERE evt_id = %s AND usr_mail = %s;", (evt_id, usr_mail))

            if cursor.rowcount == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cet événement est introuvable.")

            conn.commit()

            return {"message": "L'événement a bien été supprimé."}