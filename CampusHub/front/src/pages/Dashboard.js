import { useEffect, useState } from "react";
import { apiRequest } from "../api/client";

import { lireMatieres } from "../api/matieres";
import { lireTaches } from "../api/taches";

import { lireRetardsDashboard, lireUrgentesDashboard } from "../api/dashboard";

function Dashboard() {

    const [matieres, setMatieres] = useState([]);
    const [taches, setTaches] = useState([]);

    const [profil, setProfil] = useState(null);
    const [erreur, setErreur] = useState("");

    const [retards, setRetards] = useState([]);
    const [urgentes, setUrgentes] = useState([]);

    useEffect(() => {
        async function chargerDonnees() {
            try {
                const matieresRecues = await lireMatieres();
                const tachesRecues = await lireTaches();

                const retardsRecus = await lireRetardsDashboard();

                const urgentesRecues = await lireUrgentesDashboard();   

                setMatieres(matieresRecues);
                setTaches(tachesRecues);
                setRetards(retardsRecus);
                setUrgentes(urgentesRecues);
            } catch (erreur) {
                console.error(erreur);
            }
        }

        async function chargerProfil() {
            try {
                const resultatProfil = await apiRequest("/profil");
                setProfil(resultatProfil);
            } catch (erreur) {
                setErreur(erreur.message);
            }
        } 

        chargerProfil();
        chargerDonnees();

    }, []);

    if (erreur !== "") {return (<p>Erreur : {erreur}</p>);}


    if (profil === null) {
        return (<p>Chargement...</p>);
    }

    const nombreTerminees = taches.filter(tache => tache.tac_status === "T").length;

    const nombreEnCours = taches.filter(tache => tache.tac_status === "E").length;

    const nombreAFaire = taches.filter(tache => tache.tac_status === "A").length;

    return (
        <div>
            <h1>Dashboard CampusHub</h1>
            <p>Bienvenue {profil.usr_prenom} {profil.usr_nom}</p>
            <h2>Statistiques</h2>
            <div className="dashboard-cartes">
                <div className="dashboard-carte">📚 Matières <strong>{matieres.length}</strong></div>
                <div className="dashboard-carte">📝 Tâches <strong>{taches.length}</strong></div>
                <div className="dashboard-carte">🟢 Terminées <strong>{nombreTerminees}</strong></div>
                <div className="dashboard-carte">🟠 En cours <strong>{nombreEnCours}</strong></div>
                <div className="dashboard-carte">⚪ À faire <strong>{nombreAFaire}</strong></div>
            </div>
            <h2>Tâches en retard</h2>
            <div className="liste-dashboard">
            {
            retards.length === 0 ? (
                <div className="dashboard-ligne">
                    <p>Aucune tâche en retard.</p>
                </div>
            ) : (
                retards.map((tache) => (
                <div className="dashboard-ligne" key={tache.tac_id}>
                    <strong>{tache.tac_nom}</strong> <span>Retard : {tache.jours_retard} jours</span>
                </div>
                                ))
            )
            }
            </div>
            <h2>Tâches urgentes</h2>
            <div className="liste-dashboard">
            {
            urgentes.length === 0 ? (
                <div className="dashboard-ligne">
                    <p>Aucune tâche urgente.</p>
                </div>
            ) : (
                urgentes.map((tache) => (
                <div className="dashboard-ligne" key={tache.tac_id}>
                    <strong>{tache.tac_nom}</strong> {tache.tac_date_limite && <span>Limite : {tache.tac_date_limite}</span>}
                </div>
                                ))
            )
            }

            </div>
        </div>
    );
}

export default Dashboard;