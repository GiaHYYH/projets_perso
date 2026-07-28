import { useState } from "react";
import { apiRequest } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";


function Connexion() {

    const [email, setEmail] = useState("");
    const [motDePasse, setMotDePasse] = useState("");
    const [message, setMessage] = useState("");
    const { connexion } = useAuth();
    const navigate = useNavigate();

    async function envoyerConnexion(event) {
        event.preventDefault();
        try {
            const resultat = await apiRequest("/connexion", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({usr_mail: email, usr_mdp: motDePasse})});
            connexion(resultat.access_token);
            navigate("/");
            setMessage("Connexion réussie.");
        } catch (erreur) {
            setMessage(erreur.message);
        }
    }


    return (
        <div>
            <h1>Connexion à CampusHub</h1>
            <form onSubmit={envoyerConnexion}>
                <div>
                    <label>Adresse e-mail : </label>
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)}/>
                </div>

                <div>
                    <label>Mot de passe : </label>
                    <input type="password" value={motDePasse} onChange={(e) => setMotDePasse(e.target.value)}/>
                </div>

                <button type="submit">Se connecter </button>
            </form>

            <p>Pas encore de compte ? <Link to="/inscription">Créer un compte</Link></p>

            <p> {message}</p>
        </div>
    );
}


export default Connexion;