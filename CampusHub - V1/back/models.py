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
    """Modèle renvoyé lors de la lecture d'un utilisateur."""
    usr_mail: EmailStr
    usr_mdp: str


class MatiereCreation(BaseModel):
    """Modèle renvoyé lors de la création d'une matière."""
    mat_nom: str = Field(min_length=1, max_length=255)
    mat_couleur: str = "#FFFFFF"

    @field_validator("mat_couleur")
    def verifier_couleur(cls, couleur):
        if not re.match(r"^#[0-9a-fA-F]{6}$", couleur):
            raise ValueError("La couleur doit être un code hexadécimal valide.")
        return couleur.upper()
    
class MatiereModification(BaseModel):
    """Modèle renvoyé lors de la création d'une matière."""
    mat_nom: str = Field(min_length=1, max_length=255)
    mat_couleur: str

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


class TacheCreation(BaseModel):
    """Modèle renvoyé lors de la création d'une tâche."""
    tac_nom: str = Field(min_length=1, max_length=255)
    tac_duree: int | None = Field(default=None, gt=0)


class TacheModification(BaseModel):
    """Modèle renvoyé lors de la modification d'une tâche."""
    tac_nom: str = Field(min_length=1, max_length=255)
    tac_duree: int | None = Field(default=None, gt=0)


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
