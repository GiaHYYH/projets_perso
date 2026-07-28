import { modifierStatutTache, modifierTache } from "../api/taches";
import { afficherDuree } from "../utils/duree";
import { afficherPriorite } from "../utils/priorite";
import { afficherDate } from "../utils/date";

import { useState } from "react";

import ListeMatieresTache from "./ListeMatieresTache";

function CarteTache({ tache, onSupprimer, onStatutModifie }) {

    const [edition, setEdition] = useState(false);
    const [nom, setNom] = useState(tache.tac_nom);
    const [duree, setDuree] = useState(tache.tac_duree);
    const [date_limite, setDateLimite] = useState(tache.tac_date_limite);
    const [priorite, setPriorite] = useState(tache.tac_priorite);
    const [note, setNote] = useState(tache.tac_note);

    async function changerStatut(event) {
        try {
            await modifierStatutTache(tache.tac_id, event.target.value);
            onStatutModifie();
        } catch (erreur) {
            alert(erreur.message);
        }
    }

    function ouvrirEdition() {
        setNom(tache.tac_nom);
        setDuree(tache.tac_duree);
        setDateLimite(tache.tac_date_limite);
        setPriorite(tache.tac_priorite);
        setNote(tache.tac_note);
        setEdition(true);
    }

    async function enregistrerModification() {

        try {
            await modifierTache(tache.tac_id, {tac_nom: nom, tac_duree: duree === "" ? null : Number(duree), tac_date_limite: date_limite === "" ? null : date_limite, tac_priorite: priorite, tac_note: note === "" ? null : note});
            setEdition(false);
            onStatutModifie();
        } catch (erreur) {
            alert(erreur.message);
        }
    }

    return edition ? (
            <div className="carte-tache">
                <label>Nom : <input value={nom} onChange={(e) => setNom(e.target.value)} /></label>
                <br/><br/>
                <label>Durée : <input type="number" value={duree} onChange={(e) => setDuree(e.target.value)} /></label>
                <br/><br/>
                <label>Date Limite : <input type="date" value={date_limite} onChange={(e) => setDateLimite(e.target.value)} /></label>
                <br/><br/>
                <label>Priorité :
                    <select value={priorite} onChange={(e) => setPriorite(e.target.value)}>
                        <option value="H">Haute</option>
                        <option value="M">Moyenne</option>
                        <option value="B">Basse</option>
                    </select>
                </label>
                <br/><br/>
                <label>Note(s) : <textarea value={note} onChange={(e) => setNote(e.target.value)} /></label>
                <br/><br/>
                <button onClick={enregistrerModification}>Enregistrer</button>
                <button onClick={() => setEdition(false)}>Annuler</button>

            </div>
        ) : (
            <div className="carte-tache">
                <h3>{tache.tac_nom}</h3>

                <p>⏱ {afficherDuree(tache.tac_duree)}</p>

                <p>🗓️ {afficherDate(tache.tac_date_limite)}</p>

                <p>❗ {afficherPriorite(tache.tac_priorite)}</p>
                
                <label>Statut :
                    <select value={tache.tac_status} onChange={changerStatut}>
                        <option value="A">À faire</option>
                        <option value="E">En cours</option>
                        <option value="T">Terminée</option>
                    </select>
                </label>
                
                {
                    tache.tac_note &&
                    <p>📝 {tache.tac_note}</p>
                }
                <ListeMatieresTache tac_id={tache.tac_id}/>
                <br/>
                <button onClick={ouvrirEdition}>Modifier</button>
                <button onClick={() => onSupprimer(tache.tac_id)}>Supprimer</button>
            </div>
       );
}

export default CarteTache;