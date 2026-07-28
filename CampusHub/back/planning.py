from fastapi import APIRouter, status, HTTPException, Depends

from database import get_connection
from dependencies import get_current_user
from models import PropositionPlanning, PropositionPlanningValidation

from services.planning import (lire_evenements_jour, calculer_creneaux_libres, lire_tache, proposer_creneau, chercher_meilleur_creneau, planifier_toutes_les_taches)

from datetime import date

router = APIRouter()

@router.get("/planning/creneaux-libres")
def lire_creneaux_libres(date: date, usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
        evenements = lire_evenements_jour(conn, usr_mail, date)

        return calculer_creneaux_libres(evenements)


@router.get("/planning/proposer/{tac_id}", response_model=PropositionPlanning)
def proposition_planning(tac_id: int, usr_mail: str = Depends(get_current_user)):

    with get_connection() as conn:
        tache = lire_tache(conn, usr_mail, tac_id)
        date_limite = tache["tac_date_limite"]

        if tache is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Cette tâche est introuvable.")

        if tache["tac_duree"] is None:
            raise HTTPException(statys_code = status.HTTP_400_BAD_REQUEST, detail = "Cette tâche ne possède pas de durée.")

        if date_limite is None:
            raise HTTPException(status_code=400, detail="Cette tâche ne possède pas de date limite.")

        evenements = lire_evenements_jour(conn, usr_mail, jour)

        creneaux = calculer_creneaux_libres(evenements)

        proposition = proposer_creneau(creneaux, tache["tac_duree"])

        resultat = chercher_meilleur_creneau(conn, usr_mail, date.today(), date_limite, tache["tac_duree"])

        if resultat is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun créneau disponible avant la date limite.")

        if proposition is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Aucun créneau disponible.")

        return {"tac_id": tac_id, "tac_nom": tache["tac_nom"], "date": resultat["date"], "heure_debut": resultat["heure_debut"], "heure_fin": resultat["heure_fin"]}


@router.get("/planning/automatique", response_model=list[PropositionPlanning])
def planning_automatique(usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
        return planifier_toutes_les_taches(conn, usr_mail)


@router.post("/planning/accepter", response_model=PropositionPlanningValidation)
def accepter_proposition_planning(usr_mail: str = Depends(get_current_user)):
    with get_connection() as conn:
        ...