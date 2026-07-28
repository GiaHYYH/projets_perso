from datetime import time, date
from unittest.mock import Mock, patch, MagicMock

from services.planning import (calculer_creneaux_libres, proposer_creneau, chercher_meilleur_creneau, ordonner_taches_a_planifier, planifier_toutes_les_taches)


def test_aucun_evenement():
    resultat = calculer_creneaux_libres([])
    assert len(resultat) == 1
    assert resultat[0]["debut"] == time(8, 0)
    assert resultat[0]["fin"] == time(19, 0)


def test_un_evenement():
    evenements = [{"evt_heure_debut": time(10, 0), "evt_heure_fin": time(12, 0)}]
    resultat = calculer_creneaux_libres(evenements)

    assert len(resultat) == 2

    assert resultat[0]["debut"] == time(8, 0)
    assert resultat[0]["fin"] == time(10, 0)

    assert resultat[1]["debut"] == time(12, 0)
    assert resultat[1]["fin"] == time(19, 0)




def test_planification_simple():
    evenements = [{"evt_heure_debut": time(9, 0), "evt_heure_fin": time(11, 0)}, {"evt_heure_debut": time(14, 0), "evt_heure_fin": time(16, 0)}]

    creneaux = calculer_creneaux_libres(evenements)

    proposition = proposer_creneau(creneaux, 90)

    assert proposition is not None
    assert proposition["debut"] == time(11, 0)
    assert proposition["fin"] == time(12, 30)


def test_trouve_creneau_premier_jour():
    conn = Mock()
    with patch("services.planning.lire_evenements_jour", return_value=[]):
        resultat = chercher_meilleur_creneau(
            conn, "test@mail.com", date(2026, 7, 24), date(2026, 7, 26), 90)

    assert resultat is not None
    assert resultat["date"] == date(2026, 7, 24)
    assert resultat["heure_debut"] == time(8, 0)
    assert resultat["heure_fin"] == time(9, 30)


def test_trouve_creneau_jour_suivant():
    conn = Mock()

    def evenements(jour):
        if jour == date(2026,7,24):
            return [{"evt_heure_debut": time(8,0), "evt_heure_fin": time(19, 0)}]

        return []

    with patch("services.planning.lire_evenements_jour", side_effect=lambda conn, mail, jour: evenements(jour)):
        resultat = chercher_meilleur_creneau(conn, "test@mail.com", date(2026, 7, 24), date(2026, 7, 26), 90)

    assert resultat is not None
    assert resultat["date"] == date(2026, 7, 25)


def test_aucun_creneau_avant_date_limite():
    conn = Mock()
    with patch("services.planning.lire_evenements_jour", return_value=[{"evt_heure_debut": time(8, 0), "evt_heure_fin": time(19, 0)}]):
        resultat = chercher_meilleur_creneau(conn, "test@mail.com", date(2026, 7, 24), date(2026, 7, 26), 90)

    assert resultat is None


def test_tri_par_date_limite():
    taches = [{"tac_nom": "Projet", "tac_date_limite": date(2026, 8, 1), "tac_priorite": "H", "tac_duree": 120}, {"tac_nom": "Révision", "tac_date_limite": date(2026, 7, 25), "tac_priorite": "M", "tac_duree": 60}]
    resultat = ordonner_taches_a_planifier(taches)

    assert resultat[0]["tac_nom"] == "Révision"


def test_tri_par_priorite():
    taches = [{"tac_nom": "Lecture", "tac_date_limite": date(2026, 7, 25), "tac_priorite": "B", "tac_duree": 60}, {"tac_nom": "Examen", "tac_date_limite": date(2026, 7, 25), "tac_priorite": "H", "tac_duree": 60}]
    resultat = ordonner_taches_a_planifier(taches)

    assert resultat[0]["tac_nom"] == "Examen"

def test_tri_par_duree():
    taches = [{"tac_nom": "Petit travail", "tac_date_limite": date(2026, 7, 25), "tac_priorite": "H", "tac_duree": 30}, {"tac_nom": "Projet long", "tac_date_limite": date(2026, 7, 25), "tac_priorite": "H", "tac_duree": 180}]

    resultat = ordonner_taches_a_planifier(taches)

    assert resultat[0]["tac_nom"] == "Projet long"


def test_planifier_une_tache():
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value.__enter__.return_value = cursor
    cursor.fetchall.return_value = [(1, "Réviser Python", 90, date(2026, 7, 30), "H")]

    with patch("services.planning.chercher_meilleur_creneau", return_value={"date": date(2026, 7, 25), "heure_debut": time(9, 0), "heure_fin": time(10, 30)}):
        resultat = planifier_toutes_les_taches(conn, "test@mail.com")

    assert len(resultat) == 1
    assert resultat[0]["tac_nom"] == "Réviser Python"
    assert resultat[0]["date"] == date(2026, 7, 25)

def test_ignorer_tache_sans_creneau():
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value.__enter__.return_value = cursor
    cursor.fetchall.return_value = [(1, "Projet", 180, date(2026, 7, 30), "H")]

    with patch("services.planning.chercher_meilleur_creneau", return_value=None):
        resultat = planifier_toutes_les_taches(conn, "test@mail.com")

    assert resultat == []

def test_planifier_plusieurs_taches():
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value.__enter__.return_value = cursor
    cursor.fetchall.return_value = [(1, "Projet Web", 120, date(2026, 7, 28), "H"), (2, "Réviser SQL", 60, date(2026, 7, 30), "M")]

    propositions = [{"date": date(2026, 7, 25), "heure_debut": time(9, 0), "heure_fin": time(11, 0)}, {"date": date(2026, 7, 26), "heure_debut": time(14, 0), "heure_fin": time(15, 0)}]

    with patch("services.planning.chercher_meilleur_creneau", side_effect=propositions):
        resultat = planifier_toutes_les_taches(conn, "test@mail.com")

    assert len(resultat) == 2
    assert resultat[0]["tac_nom"] == "Projet Web"
    assert resultat[1]["tac_nom"] == "Réviser SQL"