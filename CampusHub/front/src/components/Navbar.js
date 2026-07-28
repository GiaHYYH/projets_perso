import { Link } from "react-router-dom";
import BoutonDeconnexion from "./BoutonDeconnexion";

function Navbar() {
    return (
        <nav>
            <Link to="/">Dashboard</Link>

            {" | "}

            <Link to="/matieres">Matières</Link>

            {" | "}

            <Link to="/taches">Tâches</Link>

            {" | "}

            <Link to="/calendrier">Calendrier</Link>

            {" | "}

            <Link to="/planning">Planfication Automatique</Link>

            {" | "}

            <Link to="/profil">Profil</Link>

            {" | "}

            <BoutonDeconnexion />
        </nav>
    );
}

export default Navbar;