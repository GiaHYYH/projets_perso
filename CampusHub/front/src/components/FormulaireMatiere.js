import { useState } from "react";
import { creerMatiere } from "../api/matieres";

function FormulaireMatiere({ onMatiereAjoutee }) {
    
    const [nom, setNom] = useState("");
    const [couleur, setCouleur] = useState("#FFFFFF");
    const [note, setNote] = useState("");
    const [message, setMessage] = useState("");

    async function ajouterMatiere(event) {

        event.preventDefault();

        try {
            await creerMatiere({
                mat_nom: nom,
                mat_couleur: couleur,
                mat_note: note
            });
            
            setNom("");
            setCouleur("#FFFFFF");
            setNote("");
            setMessage("Matière créée.");

            onMatiereAjoutee();
        } catch (erreur) {
            setMessage(erreur.message);
        }
    }

    return (
        <form onSubmit={ajouterMatiere}>
            <div>
                <label>Nom : </label>
                <input value={nom} onChange={(e) => setNom(e.target.value)}/>
            </div>

            <div>
                <label>Couleur : </label>
                <input type="color" value={couleur} onChange={(e) => setCouleur(e.target.value)}/>
            </div>
            <div>
                <label>Note(s) : </label>
                <textarea value={note} onChange={(e) => setNote(e.target.value)} placeholder="Ajouter une note..."/>
            </div>
            <button type="submit">Ajouter</button>
            <p>{message}</p>
        </form>
    );
}

export default FormulaireMatiere;