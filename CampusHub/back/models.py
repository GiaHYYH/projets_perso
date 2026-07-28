"""
Projet: CampusHub
Fichier: models.py
Description: Fichier contenant tous les models pydantic
Auteur: G. Eraste
Date: 9 Juillet 2026
"""
#==== IMPORTS ==================================================
import re
from pydantic import BaseModel, field_validator, EmailStr, Field
from enum import Enum
from datetime import date, time
#===============================================================

class UtilisateurCreation(BaseModel):
    """Modèle renvoyé lors de la création d'un utilisateur."""
    usr_mail: EmailStr
    usr_mdp: str = Field(min_length=14)
    usr_nom: str | None = None
    usr_prenom: str | None = None 
    usr_niveau: str 
    usr_formation: str 

class UtilisateurConnexion(BaseModel):
    """Modèle renvoyé lors de la connexion d'un utilisateur."""
    usr_mail: EmailStr
    usr_mdp: str

class UtilisateurModification(BaseModel):
    usr_nom: str | None = None
    usr_prenom: str | None = None
    usr_niveau: str
    usr_formation: str


class Utilisateur(BaseModel):
    """Modèle renvoyé lors de la lecture du profil utilisateur"""
    usr_mail: EmailStr
    usr_nom: str | None = None
    usr_prenom: str | None = None 
    usr_niveau: str 
    usr_formation: str 


class MatiereCreation(BaseModel):
    """Modèle renvoyé lors de la création d'une matière."""
    mat_nom: str = Field(min_length=1, max_length=255)
    mat_couleur: str = "#FFFFFF"
    mat_note: str | None = None

    @field_validator("mat_couleur")
    def verifier_couleur(cls, couleur):
        if not re.match(r"^#[0-9a-fA-F]{6}$", couleur):
            raise ValueError("La couleur doit être un code hexadécimal valide.")
        return couleur.upper()
    
class MatiereModification(BaseModel):
    """Modèle renvoyé lors de la création d'une matière."""
    mat_nom: str = Field(min_length=1, max_length=255)
    mat_couleur: str
    mat_note: str | None = None

    @field_validator("mat_couleur")
    def verifier_couleur(cls, couleur):
        if not re.match(r"^#[0-9a-fA-F]{6}$", couleur):
            raise ValueError("La couleur doit être un code hexadécimal valide.")
        return couleur.upper()

class Matiere(BaseModel):
    """Modèle renvoyé lors de la lecture d'une matière."""
    mat_id: int
    mat_nom: str 
    mat_couleur: str
    mat_note: str | None = None

class PrioriteTache(str, Enum):
    BASSE = "B"
    MOYENNE = "M"
    HAUTE = "H"

class TacheCreation(BaseModel):
    """Modèle renvoyé lors de la création d'une tâche."""
    tac_nom: str = Field(min_length=1, max_length=255)
    tac_duree: int | None = Field(default=None, gt=0)
    tac_date_limite: date | None = None
    tac_priorite: PrioriteTache = PrioriteTache.MOYENNE
    tac_note: str | None = None


class TacheModification(BaseModel):
    """Modèle renvoyé lors de la modification d'une tâche."""
    tac_nom: str = Field(min_length=1, max_length=255)
    tac_duree: int | None = Field(default=None, gt=0)
    tac_date_limite: date | None = None
    tac_priorite: PrioriteTache
    tac_note: str | None = None


class StatutTache(str, Enum):
    """Modèle renvoyé lors de la lecture du statut d'une tâche."""
    A_FAIRE = "A"
    EN_COURS = "E"
    TERMINEE = "T"



class TacheStatutModification(BaseModel):
    """Modèle renvoyé lors de la modification du statut d'une tâche."""
    tac_status: StatutTache


class Tache(BaseModel):
    """Modèle renvoyé lors de la lecture d'une tâche."""
    tac_id: int 
    tac_nom: str
    tac_duree: int | None = None
    tac_status: StatutTache
    tac_date_limite: date | None = None
    tac_priorite: PrioriteTache
    tac_note: str | None = None


class Dashboard(BaseModel):
    """Modèle renvoyé lors de la lecture du tableau de bord."""
    nombre_total_taches: int
    taches_a_faire: int
    taches_en_cours: int 
    taches_terminees: int 
    temps_total_estime: int 
    taches_urgentes: int 


class DashboardMatiere(BaseModel):
    mat_id: int
    mat_nom: str
    nombres_taches: int
    temps_total_estime: int


class DashboardRetard(BaseModel):
    tac_id: int
    tac_nom: str 
    tac_date_limite: date 
    tac_priorite: PrioriteTache
    jours_retard: int  

class DashboardUrgente(BaseModel):
    tac_id: int
    tac_nom: str
    tac_date_limite: date | None = None
    tac_priorite: PrioriteTache

class TypeEvenement(str, Enum):
    COURS = "COURS"
    TD = "TD"
    TP = "TP"
    EXAMEN = "EXAMEN"
    TRAVAIL = "TRAVAIL"
    PERSONNEL = "PERSONNEL"
    SPORT = "SPORT"
    AUTRE = "AUTRE"

class EvenementCreation(BaseModel):
    evt_nom: str = Field(min_length=1, max_length=255)
    evt_date: date
    evt_heure_debut: time
    evt_heure_fin: time
    evt_type: TypeEvenement
    evt_description: str | None = None
    evt_couleur: str = "#3B82F6"
    @field_validator("evt_couleur")
    def verifier_couleur(cls, couleur):
        if not re.match(r"^#[0-9a-fA-F]{6}$", couleur):
            raise ValueError("La couleur doit être un code hexadécimal valide.")
        return couleur.upper()

    @field_validator("evt_heure_fin")
    def verifier_heures(cls, heure_fin, info):
        heure_debut = info.data.get("evt_heure_debut")

        if heure_debut and heure_fin <= heure_debut:
            raise ValueError(
                "L'heure de fin doit être après l'heure de début."
            )

        return heure_fin

class EvenementModification(EvenementCreation):
    pass

class Evenement(BaseModel):
    evt_id: int
    evt_nom: str
    evt_date: date
    evt_heure_debut: time
    evt_heure_fin: time
    evt_type: TypeEvenement
    evt_description: str | None = None
    evt_couleur: str


class PropositionPlanning(BaseModel):
    tac_id: int
    tac_nom: str
    date: date 
    heure_debut: time 
    heure_fin: time 


class PropositionPlanningValidation(BaseModel):
    tac_id: int
    date: date
    heure_debut: time
    heure_fin: time