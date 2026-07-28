import { useState } from "react";
import { creerEvenement } from "../api/evenements";

function FormulaireEvenement({ onEvenementAjoute }) {
    
    const [nom, setNom] = useState("");
    const [date, setDate] = useState("");
    const [heureDebut, setHeureDebut] = useState("");
    const [heureFin, setHeureFin] = useState("");
    const [type, setType] = useState("COURS");
    const [description, setDescription] = useState("");
    const [couleur, setCouleur] = useState("#3B82F6");

    const [message, setMessage] = useState("");

    async function ajouterEvenement(event) {

        event.preventDefault();

        try {
            await creerEvenement({
                evt_nom: nom,
                evt_date: date,
                evt_heure_debut: heureDebut,
                evt_heure_fin: heureFin,
                evt_type: type,
                evt_description: description,
                evt_couleur: couleur
            });
            
            setNom("");
            setDate("");
            setHeureDebut("");
            setHeureFin("");
            setType("COURS");
            setDescription("");
            setCouleur("#3B82F6");
            setMessage("Événement créé.");

            onEvenementAjoute();
        } catch (erreur) {
            setMessage(erreur.message);
        }
    }

    return (
        <form onSubmit={ajouterEvenement}>
            <div>
                <label>Nom : </label>
                <input value={nom} onChange={(e) => setNom(e.target.value)}/>
            </div>
            <div>
                <label>Date :</label>
                <input type="date"  value={date} onChange={(e) => setDate(e.target.value)} />
            </div>
            <div>
                <label>Heure de début :</label>
                <input type="time" value={heureDebut} onChange={(e) => setHeureDebut(e.target.value)} />
            </div>
            <div>
                <label>Heure de fin :</label>
                <input type="time" value={heureFin} onChange={(e) => setHeureFin(e.target.value)} />
            </div>
            <div>
                <label>Description :</label>
                <textarea value={description} onChange={(e) => setDescription(e.target.value)} />
            </div>
            <div>
                <select value={type} onChange={(e) => setType(e.target.value)}>
                    <option value="COURS">Cours</option>
                    <option value="TD">TD</option>
                    <option value="TP">TP</option>
                    <option value="EXAMEN">Examen</option>
                    <option value="TRAVAIL">Travail</option>
                    <option value="PERSONNEL">Personnel</option>
                    <option value="SPORT">Sport</option>
                    <option value="AUTRE">Autre</option>
                </select>
            </div>
            <div>
                <input type="color" value={couleur} onChange={(e) => setCouleur(e.target.value)} />
            </div>
            <button type="submit">Ajouter</button>
            <p>{message}</p>
        </form>
    );
}

export default FormulaireEvenement;