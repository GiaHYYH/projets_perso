import { useEffect, useState } from "react";
//import { apiRequest } from "../api/client";
import { afficherDate } from "../utils/date";
import { supprimerEvenement, lireEvenements } from "../api/evenements";

import FormulaireEvenement from "../components/FormulaireEvenement";
import CarteEvenement from "../components/CarteEvenement";

function Calendrier() {

    const [evenements, setEvenements] = useState([]);

    
    async function chargerEvenements() {
        try {
            const resultat = await lireEvenements();
            setEvenements(resultat);
        } catch (erreur) {
            alert(erreur.message);
        }
    }
    
    useEffect(() => {
        chargerEvenements();
    }, []);
    
    async function supprimer(evt_id) {
        if (!window.confirm("Supprimer cet événement ?")) {
            return;
        }

        try {
            await supprimerEvenement(evt_id);
            await chargerEvenements();
        } catch (erreur) {
            alert(erreur.message);
        }
    }

    const groupes = {};

    evenements.forEach((evt) => {
        if (!groupes[evt.evt_date]) {
            groupes[evt.evt_date] = [];
        }

        groupes[evt.evt_date].push(evt);
    });


    return (
        <div>
            <h1>Calendrier</h1>
            <FormulaireEvenement onEvenementAjoute={chargerEvenements} />
            
            <div className="liste-cartes">
                {evenements.length === 0 ? (
                    <p>Aucun événement.</p>
                ) : (
                    Object.keys(groupes).map((date) => (
                        <div key={date}>
                            <h2>{afficherDate(date)}</h2>
                            {groupes[date].map((evt) => (
                                <CarteEvenement
                                    key={evt.evt_id}
                                    evenement={evt}
                                    onSupprimer={supprimer}
                                    onEventModifie={chargerEvenements}
                                />
                            ))}
                        </div>
                    ))
                )}
            </div>
        </div>
    );

}

export default Calendrier;