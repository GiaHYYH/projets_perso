import { apiRequest } from "./client";

export async function supprimerProfil() {
    return await apiRequest("/profil", {method: "DELETE"});
}