import { useState } from "react";
import { apiRequest } from "../api/client";
import { useNavigate } from "react-router-dom";

function Inscription() {

    const navigate = useNavigate();
    const [formulaire, setFormulaire] = useState({usr_mail: "", usr_mdp: "", usr_nom: "", usr_prenom: "", usr_niveau: "", usr_formation: ""});
    const [message, setMessage] = useState("");

    function modifierChamp(event) {
        setFormulaire({...formulaire, [event.target.name]: event.target.value});
    }

    async function envoyerInscription(event) {
        event.preventDefault();
        try {
            await apiRequest("/utilisateurs", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(formulaire)});
            setMessage("Compte créé avec succès.");
            setTimeout(() => {
                navigate("/connexion");
            }, 1500);
        } catch (erreur) {
            setMessage(erreur.message);
        }
    }

    return (
        <div>
            <h1>Créer un compte</h1>
            <form onSubmit={envoyerInscription}>
                <input name="usr_nom" placeholder="Nom" value={formulaire.usr_nom} onChange={modifierChamp} />
                <br/><br/>
                <input name="usr_prenom" placeholder="Prénom" value={formulaire.usr_prenom} onChange={modifierChamp} />
                <br/><br/>
                <input type="email" name="usr_mail" type="email" placeholder="Adresse e-mail" value={formulaire.usr_mail} onChange={modifierChamp} />
                <br/><br/>
                <input name="usr_mdp" type="password" placeholder="Mot de passe" value={formulaire.usr_mdp} onChange={modifierChamp} />
                <br/><br/>
                <input name="usr_niveau" placeholder="Niveau" value={formulaire.usr_niveau} onChange={modifierChamp} />
                <br/><br/>
                <input name="usr_formation" placeholder="Formation" value={formulaire.usr_formation} onChange={modifierChamp} />
                <br/><br/>
                <button type="submit">Créer mon compte</button>
            </form>
            <p>{message}</p>
        </div>
    );
}


export default Inscription;