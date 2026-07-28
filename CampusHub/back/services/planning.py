from datetime import time, datetime, timedelta, date

def calculer_creneaux_libres(evenements):
    """Calcule les créneax libres d'une journée"""
    debut_journee = time(8,0)
    fin_journee = time(19, 0)

    heure_courante = debut_journee

    creneaux = []

    for evenement in evenements:
        if evenement["evt_heure_debut"] > heure_courante:
            creneaux.append({"debut": heure_courante, "fin": evenement["evt_heure_debut"]})

        heure_courante = evenement["evt_heure_fin"]

    if heure_courante < fin_journee:
        creneaux.append({"debut": heure_courante, "fin": fin_journee})

    return creneaux


def lire_evenements_jour(conn, usr_mail, date):
    with conn.cursor() as cursor:
        cursor.execute("SELECT evt_heure_debut, evt_heure_fin FROM t_evenement_evt WHERE usr_mail = %s AND evt_date = %s ORDER BY evt_heure_debut;", (usr_mail, date))
        resultats = cursor.fetchall()

        return [{"evt_heure_debut": resultat[0], "evt_heure_fin": resultat[1]} for resultat in resultats]


def proposer_creneau(creneaux, duree_minutes):
    for creneau in creneaux:
        debut = datetime.combine(datetime.today(), creneau["debut"])
        fin = datetime.combine(datetime.today(), creneau["fin"])

        duree = (fin - debut).total_seconds() / 60

        if duree >= duree_minutes:
            return {"debut": creneau["debut"], "fin": (debut + timedelta(minutes=duree_minutes)).time()}

    return None


def lire_tache(conn, usr_mail, tac_id):
    with conn.cursor() as cursor:
        cursor.execute("SELECT tac_nom, tac_duree FROM t_tache_tac WHERE tac_id = %s AND usr_mail = %s;", (tac_id, usr_mail))
        resultat = cursor.fetchone()

    if resultat is None:
        return None

    return {"tac_nom": resultat[0], "tac_duree": resultat[1]}


def chercher_meilleur_creneau(conn, usr_mail, date_debut, date_limite, duree):
    jour = date_debut
    while jour <= date_limite:
        evenements = lire_evenements_jour(conn, usr_mail, jour)
        creneaux = calculer_creneaux_libres(evenements)
        proposition = proposer_creneau(creneaux, duree)

        if proposition is not None:
            return {"date": jour, "heure_debut": proposition["debut"], "heure_fin": proposition["fin"]}

        jour += timedelta(days=1)

    return None


def ordonner_taches_a_planifier(taches):
    """
    Trie les tâches selon:
    1. Date limite la plus proche
    2. Priorités
    3. Plus longue durée
    """
    order_priorite = {"H": 0, "M": 1, "B": 2}

    DATE_MAX = date.max

    return sorted(taches, key=lambda tache: (tache["tac_date_limite"] or DATE_MAX, order_priorite[tache["tac_priorite"]], -(tache["tac_duree"] or 0)))


def planifier_toutes_les_taches(conn, usr_mail):
    with conn.cursor() as cursor:
        cursor.execute("SELECT tac_id, tac_nom, tac_duree, tac_date_limite, tac_priorite FROM t_tache_tac WHERE usr_mail = %s AND tac_status <> 'T' AND tac_duree IS NOT NULL AND tac_date_limite IS NOT NULL;", (usr_mail,))
        resultats = cursor.fetchall()

        taches = []

        for resultat in resultats:
            taches.append({"tac_id": resultat[0], "tac_nom": resultat[1], "tac_duree": resultat[2], "tac_date_limite": resultat[3], "tac_priorite": resultat[4]})

        taches_tri = ordonner_taches_a_planifier(taches)

        propositions = []

        for tache in taches_tri:
            resultat = chercher_meilleur_creneau(conn, usr_mail, date.today(), tache["tac_date_limite"], tache["tac_duree"])

            if resultat is None:
                continue

            propositions.append({"tac_id": tache["tac_id"], "tac_nom": tache["tac_nom"], "date": resultat["date"], "heure_debut": resultat["heure_debut"], "heure_fin": resultat["heure_fin"]})

        return propositions