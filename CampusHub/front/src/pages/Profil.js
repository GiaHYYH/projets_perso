import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { apiRequest } from "../api/client";
import { supprimerProfil } from "../api/profil";
import { useAuth } from "../context/AuthContext";


function Profil() {

    const [profil, setProfil] = useState(null);
    const [erreur, setErreur] = useState("");
    
    const [modification, setModification] = useState(false);
    const [formulaire, setFormulaire] = useState({usr_nom: "", usr_prenom: "", usr_niveau: "", usrf_formation: ""});

    const navigate = useNavigate();
    const { deconnexion } = useAuth();

    useEffect(() => {
        async function chargerProfil() {
            try {
                const resultatProfil = await apiRequest("/profil");
                setProfil(resultatProfil);


            } catch (erreur) {
                setErreur(erreur.message);
            }
        } chargerProfil();}, []);

    function activerModification() {
        setFormulaire({usr_nom: profil.usr_nom || "", usr_prenom: profil.usr_prenom || "", usr_niveau: profil.usr_niveau, usr_formation: profil.usr_formation});
        setModification(true);
    }

    function modifierChamp(event) {
        setFormulaire({...formulaire, [event.target.name]: event.target.value});
    }

    async function enregistrerModification() {
        try {
            await apiRequest("/profil", {method: "PUT", headers: {"Content-Type": "application/json"}, body: JSON.stringify(formulaire)});
            const nouveauProfil = await apiRequest("/profil");
            setProfil(nouveauProfil);
            setModification(false);
        } catch (erreur) {
            setErreur(erreur.message);
        }
    }

    function annulerModification() {
        setModification(false);
    }

    async function supprimerCompte() {
        const confirmation = window.confirm("Êtes-vous sûr(e) de vouloir supprimer votre compte? Cette action est définitive.");

        if (!confirmation) {
            return;
        }

        try {
            await supprimerProfil();
            deconnexion();
            navigate("/connexion");
        } catch (erreur) {
            console.error(erreur);
            alert("Une erreur est survenue lors de la suppression du compte.");
        }
    }

    if (erreur !== "") {
        return (<p>Erreur : {erreur}</p>);
    }


    if (profil === null) {
        return (<p>Chargement...</p>);
    }


    return (
        <div>
            <h1>Mon profil</h1>
            {
            !modification ? (
                <div className="profil-carte">
                    <p><strong>Nom :</strong> {profil.usr_nom}</p>
                    <p><strong>Prénom :</strong> {profil.usr_prenom}</p>
                    <p><strong>Adresse e-mail :</strong> {profil.usr_mail}</p>
                    <p><strong>Niveau :</strong> {profil.usr_niveau}</p>
                    <p><strong>Formation :</strong> {profil.usr_formation} </p>

                    <button onClick={activerModification}>Modifier</button>
                </div>
            ) : (
                <div className="profil-carte">
                    <h2>Modifier mon profil</h2>
                    <label>Nom : <input name="usr_nom" value={formulaire.usr_nom} onChange={modifierChamp} /></label>

                    <br />

                    <label>Prénom : <input name="usr_prenom" value={formulaire.usr_prenom} onChange={modifierChamp} /></label>

                    <br />

                    <label>Niveau : <input name="usr_niveau" value={formulaire.usr_niveau} onChange={modifierChamp} /></label>

                    <br />

                    <label>Formation : <input name="usr_formation" value={formulaire.usr_formation} onChange={modifierChamp} /></label>

                    <br />

                    <button onClick={enregistrerModification}>Enregistrer</button>

                    <button onClick={annulerModification}>Annuler</button>
                </div>
            )
            }
            <div className="zone-danger">
                <h2>⚠️</h2>
                <p><strong>La suppression de votre compte est définitive.</strong></p>
                <button onClick={supprimerCompte}>Supprimer mon compte</button>
            </div>
        </div>
    );
}

export default Profil;