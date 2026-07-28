import { useEffect, useState } from "react";

import { lireMatieres, supprimerMatiere } from "../api/matieres";

import FormulaireMatiere from "../components/FormulaireMatiere";
import CarteMatiere from "../components/CarteMatiere";

function Matieres() {

    const [matieres, setMatieres] = useState([]);

    async function chargerMatieres() {
        try {

            const resultat = await lireMatieres();
    
            setMatieres(resultat);
        } catch (erreur) {
            alert(erreur.message);
        }
    }

    useEffect(() => {
        chargerMatieres();
    }, []);

    async function supprimer(mat_id) {
        if(!window.confirm("Supprimer cette matière?")) {
            return;
        }

        try {
            await supprimerMatiere(mat_id);
            await chargerMatieres();
        } catch (erreur) {
            alert(erreur.message);
        }
    }


    return (
        <div>
            <h1>Mes matières</h1>

            <FormulaireMatiere onMatiereAjoutee={chargerMatieres} />

            <div className="liste-cartes">

                {matieres.map((matiere) => (
                    <CarteMatiere key={matiere.mat_id} matiere={matiere} onSupprimer={supprimer} onMatiereModifie={chargerMatieres}/>
                ))}
            </div>
        </div>
    );
}

export default Matieres;