import { useEffect, useState } from "react";
import { lireMatieresTache, lierTacheMatiere, supprimerLienTacheMatiere } from "../api/taches";
import { lireMatieres } from "../api/matieres";

function ListeMatieresTache({ tac_id }) {
    const [matieres, setMatieres] = useState([]);
    const [matieresDisponibles, setMatieresDisponibles] = useState([]);
    const [matiereSelectionnee, setMatiereSelectionnee] = useState("");

    async function chargerMatieres() {
        try {
            const resultat = await lireMatieresTache(tac_id);
            setMatieres(resultat);
        } catch (erreur) {
            console.error(erreur);
        }
    }

    async function chargerMatieresDisponibles() {
        try {
            const resultat = await lireMatieres();
            setMatieresDisponibles(resultat);
        } catch (erreur) {
            console.error(erreur);
        }
    }

    async function ajouterMatiere() {
        if (matiereSelectionnee === "") {
            return;
        }

        try {
            await lierTacheMatiere(tac_id, Number(matiereSelectionnee));
            await chargerMatieres();
            setMatiereSelectionnee("");
        } catch (erreur) {
            alert(erreur.message);
        }
    }

    async function supprimerMatiere(mat_id) {
        try {
            await supprimerLienTacheMatiere(tac_id, mat_id);
            await chargerMatieres();
        } catch (erreur) {
            alert(erreur.message);
        }
    }

    useEffect(() => {
        chargerMatieres();
        chargerMatieresDisponibles();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [tac_id]);

    return (
        <div>
            <strong>Matières : </strong>

            <ul>
                {matieres.map((matiere) => (
                    <li key={matiere.mat_id}>{matiere.mat_nom} <button onClick={() => supprimerMatiere(matiere.mat_id)}>❌</button></li>
                ))}
            </ul>
            <br />
            <select value={matiereSelectionnee} onChange={(e) => setMatiereSelectionnee(e.target.value)}>
                <option value="">Choisir une matière </option>
                {matieresDisponibles.map((matiere) => (
                    <option key={matiere.mat_id} value={matiere.mat_id}>{matiere.mat_nom}</option>
                ))}
            </select>

            <button onClick={ajouterMatiere}>Ajouter</button>
        </div>
    );
}

export default ListeMatieresTache;