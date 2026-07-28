import { useEffect, useState } from "react";

import { lireTaches, supprimerTache } from "../api/taches";

import FormulaireTache from "../components/FormulaireTache";
import CarteTache from "../components/CarteTache";

function Taches() {

    const [taches, setTaches] = useState([]);

    async function chargerTaches() {
        try {

            const resultat = await lireTaches();
    
            setTaches(resultat);
        } catch (erreur) {
            alert(erreur.message);
        }
    }

    useEffect(() => {
        chargerTaches();
    }, []);

    async function supprimer(tac_id) {
        if(!window.confirm("Supprimer cette tâche?")) {
            return;
        }

        try {
            await supprimerTache(tac_id);
            await chargerTaches();
        } catch (erreur) {
            alert(erreur.message);
        }
    }


    return (
        <div>
            <h1>Mes tâches</h1>

            <FormulaireTache onTacheAjoutee={chargerTaches} />

            <div className="liste-cartes">
                {taches.map((tache) => (
                        <CarteTache key={tache.tac_id} tache={tache} onSupprimer={supprimer} onStatutModifie={chargerTaches}/>
                    ))}
            </div>
        </div>
    );
}

export default Taches;