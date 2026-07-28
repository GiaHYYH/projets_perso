import { useState } from "react";
import { creerTache } from "../api/taches";

function FormulaireTache({ onTacheAjoutee }) {
    
    const [formulaire, setFormulaire] = useState({tac_nom: "", tac_duree: "", tac_date_limite: "", tac_priorite: "M", tac_note: ""});
    const [message, setMessage] = useState("");

    async function ajouterTache(event) {

        event.preventDefault();

        try {
            await creerTache({
                tac_nom: formulaire.tac_nom,
                tac_duree: formulaire.tac_duree,
                tac_date_limite: formulaire.tac_date_limite === "" ? null : formulaire.tac_date_limite,
                tac_priorite: formulaire.tac_priorite,
                tac_note: formulaire.tac_note === "" ? null : formulaire.tac_note
            });
            
            setFormulaire({
                tac_nom: "",
                tac_duree: "",
                tac_date_limite: "",
                tac_priorite: "M",
                tac_note: ""
            });
            setMessage("Tâche créée.");

            onTacheAjoutee();
        } catch (erreur) {
            setMessage(erreur.message);
        }
    }

    function modifierChamp(event) {
        setFormulaire({...formulaire, [event.target.name]: event.target.value});
    }

    return (
        <form onSubmit={ajouterTache}>
            <div>
                <label>Nom : </label>
                <input name="tac_nom" value={formulaire.tac_nom} required onChange={modifierChamp}/>
            </div>

            <div>
                <label>Durée : </label>
                <input name="tac_duree" type="number" min="1" value={formulaire.tac_duree} onChange={modifierChamp}/>
            </div>
            <div>
                <label>Date limite : </label>
                <input name="tac_date_limite" type="date" value={formulaire.tac_date_limite} onChange={modifierChamp} />
            </div>
            <div>
                <label>Priorité : </label>
                <select name="tac_priorite" value={formulaire.tac_priorite} onChange={modifierChamp}>
                    <option value="H">Haute</option>
                    <option value="M">Moyenne</option>
                    <option value="B">Basse</option>
                </select>
            </div>
            <div>
                <label>Note(s) : </label>
                <textarea name="tac_note" value={formulaire.tac_note} onChange={modifierChamp} />
            </div>
            <button type="submit">Ajouter</button>
            <p>{message}</p>
        </form>
    );
}

export default FormulaireTache;