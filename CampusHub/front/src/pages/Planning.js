import { useEffect, useState } from "react";
import { recupererPlanningAutomatique } from "../api/planning";
import { afficherDate} from "../utils/date";

function Planning() {
    const [propositions, setPropositions] = useState([]);
    const [chargement, setChargement] = useState(true);
    const [erreur, setErreur] = useState("");

    useEffect(() => {
        chargerPlanning();
    }, []);

    async function chargerPlanning() {
        try {
            const resultat = await recupererPlanningAutomatique();
            setPropositions(resultat);
        } catch (e) {
            setErreur(e.message);
        } finally {
            setChargement(false);
        }
    }

    if (chargement) {
        return <p>Chargement...</p>;
    }

    if (erreur) {
        return <p>{erreur}</p>;
    }

    return (
        <div>
            <h1>Planification automatique</h1>

            {propositions.length === 0 ? (
                <p>Aucune proposition disponible.</p>
            ) : (
                propositions.map((proposition) => (
                    <div
                        key={proposition.tac_id}
                        style={{border: "1px solid #ddd", padding: "15px", marginBottom: "15px", borderRadius: "8px"}}>
                        <h3>{proposition.tac_nom}</h3>
                        <p>📅 {afficherDate(proposition.date)}</p>
                         <p>🕒 {proposition.heure_debut}{" - "}{proposition.heure_fin}</p>
                        <button disabled>Accepter (bientôt disponible)</button>
                    </div>
                ))
            )}
        </div>
    );
}

export default Planning;