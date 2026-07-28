const API_URL = "http://127.0.0.1:8000/";

export async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem("token");

    const headers = {"Content-Type": "application/json", ...options.headers};

    if (token !== null) {
        headers["Authorization"] = `Bearer ${token}`;
    }
    
    
    
    const response = await fetch(API_URL + endpoint, {...options, headers});

    const data = await response.json();

    if (!response.ok) {
        if (data.detail) {
            if (Array.isArray(data.detail)) {
                throw new Error(data.detail[0].msg);
            }
            throw new Error(data.detail);
        }
        throw new Error("Une erreur est survenue.");
    }

    return data;
}