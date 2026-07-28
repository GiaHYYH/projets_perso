import { useState } from "react";

import { modifierEvenement } from "../api/evenements";
import { afficherDate } from "../utils/date";

function CarteEvenement({ evenement, onSupprimer, onEventModifie}) {

    const [edition, setEdition] = useState(false);
    const [nom, setNom] = useState(evenement.evt_nom);
    const [type, setType] = useState(evenement.evt_type);
    const [date, setDate] = useState(evenement.evt_date);
    const [heureDebut, setHeureDebut] = useState(evenement.evt_heure_debut);
    const [heureFin, setHeureFin] = useState(evenement.evt_heure_fin);
    const [description, setDescription] = useState(evenement.evt_description);
    const [couleur, setCouleur] = useState(evenement.evt_couleur);

    async function enregistrerModification() {
        try {
            await modifierEvenement(evenement.evt_id, {evt_nom: nom, evt_type: type, evt_date: date, evt_heure_debut: heureDebut, evt_heure_fin: heureFin, evt_description: description, evt_couleur: couleur});
            setEdition(false);
            onEventModifie();
        } catch (erreur) {
            alert(erreur.message);
        }
    }

    function icone(type) {
        switch (type) {
            case "COURS":
                return "📚";
            case "TD":
                return "📝";
            case "TP":
                return "💻";
            case "EXAMEN":
                return "🎓";
            case "SPORT":
                return "🏋️";
            case "TRAVAIL":
                return "💼";
            case "PERSONNEL":
                return "🏠";
            default:
                return "📅";
        }
    }

    return (
        <div className="carte-evenement" style={{border: "1px solid #ddd", borderLeft: `20px solid ${evenement.evt_couleur}`, marginBottom: "15px", padding: "10px"}}>
            {
            edition ? (
                <div>
                    <label>Nom : <input value={nom} onChange={(e) => setNom(e.target.value)}/></label>
                    <br />
                    <label>Type :
                        <select value={type} onChange={(e) => setType(e.target.value)}>
                            <option value="COURS">Cours</option>
                            <option value="TD">TD</option>
                            <option value="TP">TP</option>
                            <option value="EXAMEN">Examen</option>
                            <option value="SPORT">Sport</option>
                            <option value="TRAVAIL">Travail</option>
                            <option value="PERSONNEL">Personnel</option>
                        </select>
                    </label>
                    <br />
                    <label>Date : <input type="date" value={date} onChange={(e) => setDate(e.target.value)}/></label>
                    <br />
                    <label>Heure début : <input type="time" value={heureDebut} onChange={(e) => setHeureDebut(e.target.value)}/></label>
                    <br />
                    <label>Heure fin : <input type="time" value={heureFin} onChange={(e) => setHeureFin(e.target.value)}/></label>
                    <br />
                    <label>Couleur : <input type="color" value={couleur} onChange={(e) => setCouleur(e.target.value)}/></label>
                    <br />
                    <label>Description : <textarea value={description} onChange={(e) => setDescription(e.target.value)}/></label>
                    <br />
                    <button onClick={enregistrerModification}>Enregistrer</button>
                    <button onClick={() => setEdition(false)}>Annuler</button>
                </div>
            ) : (
                <div>
                    <h3>{icone(evenement.evt_type)} {evenement.evt_nom}</h3>
                    <p>📅 {afficherDate(evenement.evt_date)}</p>
                    <p>🕒 {evenement.evt_heure_debut} - {evenement.evt_heure_fin}</p>
                    <p>Type : {evenement.evt_type}</p>
                    {evenement.evt_description && (
                        <p>📝 {evenement.evt_description}</p>
                    )}
                    <button onClick={() => setEdition(true)}>Modifier</button>
                    <button onClick={() => onSupprimer(evenement.evt_id)}>Supprimer</button>
                </div>
            )
            }
        </div>
    );
}

export default CarteEvenement;