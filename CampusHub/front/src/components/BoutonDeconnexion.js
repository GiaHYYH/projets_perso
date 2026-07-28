import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";


function BoutonDeconnexion() {

    const { deconnexion } = useAuth();

    const navigate = useNavigate();

    function quitter() {

        deconnexion();

        navigate("/connexion");

    }

    return (
        <button onClick={quitter}>Déconnexion</button>
    );
}

export default BoutonDeconnexion;