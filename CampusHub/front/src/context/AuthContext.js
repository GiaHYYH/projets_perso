import { createContext, useContext, useState } from "react";


const AuthContext = createContext();


export function AuthProvider({ children }) {

    const [token, setToken] = useState(localStorage.getItem("token"));

    function connexion(nouveauToken) {
        localStorage.setItem("token", nouveauToken);
        setToken(nouveauToken);
    }

    function deconnexion() {
        localStorage.removeItem("token");
        setToken(null);
    }

    return (<AuthContext.Provider value={{token, connexion, deconnexion}}>{children}</AuthContext.Provider>);
}


export function useAuth() {
    return useContext(AuthContext);
}