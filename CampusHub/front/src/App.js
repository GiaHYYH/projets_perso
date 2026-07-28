import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";

import Dashboard from "./pages/Dashboard";
import Connexion from "./pages/Connexion";
import Inscription from "./pages/Inscription";
import Matieres from "./pages/Matieres";
import Taches from "./pages/Taches";
import Profil from "./pages/Profil";
import Calendrier from "./pages/Calendrier";
import Planning from "./pages/Planning";

import { Navigate } from "react-router-dom";

import "./App.css";

import { useAuth } from "./context/AuthContext";

function App() {

    const { token } = useAuth();


    return (

        <Routes>
            {/* Pages accessibles sans connexion */}
            <Route path="/connexion" element={<Connexion />} />
            <Route path="/inscription" element={<Inscription />} />
            {/* Pages protégées */}
            {
            token && (
                <>
                    <Route path="/" element={token ? <Layout><Dashboard /></Layout> : <Navigate to="/connexion" replace />} />

                    <Route path="/matieres" element={<Layout><Matieres /></Layout>} />

                    <Route path="/taches" element={<Layout><Taches /></Layout>} />

                    <Route path="/profil" element={<Layout><Profil /></Layout>} />

                    <Route path="/calendrier" element={<Layout><Calendrier /></Layout>} />

                    <Route path="/planning" element={<Layout><Planning /></Layout>} />
                </>
            )}

        </Routes>

    );

}


export default App;