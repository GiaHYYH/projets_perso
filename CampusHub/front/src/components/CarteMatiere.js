import { useState } from "react";

import { modifierMatiere } from "../api/matieres";


function CarteMatiere({ matiere, onSupprimer, onMatiereModifie }) {

    const [edition, setEdition] = useState(false);
    const [nom, setNom] = useState(matiere.mat_nom);
    const [couleur, setCouleur] = useState(matiere.mat_couleur);
    const [note, setNote] = useState(matiere.mat_note);

    async function enregistrerModification() {
        try {
            await modifierMatiere(matiere.mat_id, {mat_nom: nom, mat_couleur: couleur, mat_note: note});
            setEdition(false);
            onMatiereModifie();
        } catch (erreur) {
            alert(erreur.message);
        }
    }

    return (
        <div className="carte-matiere">
            {
            edition ? (
                <div>
                    <label>Nom : <input value={nom} onChange={(e) => setNom(e.target.value)}/></label>
                    <br />
                    <label>Couleur : <input type="color" value={couleur} onChange={(e) => setCouleur(e.target.value)}/></label>
                    <br />
                    <label>Note(s) : <textarea value={note} onChange={(e) => setNote(e.target.value)}/></label>
                    <br />
                    <button onClick={enregistrerModification}>Enregistrer</button>
                    <button onClick={() => setEdition(false)}>Annuler</button>
                </div>
            ) : (
                <div>
                    <h3>{matiere.mat_nom}</h3>
                    <div className="pastille-couleur" style={{backgroundColor: matiere.mat_couleur}}></div>
                    <br />
                    {
                        matiere.mat_note &&
                        <p>📝 {matiere.mat_note}</p>
                    }
                    <button onClick={() => setEdition(true)}>Modifier</button>
                    <button onClick={() => onSupprimer(matiere.mat_id)}>Supprimer</button>
                </div>
            )
            }
        </div>

    );

}


export default CarteMatiere;