import { apiRequest } from "./client";


export async function modifierProfil(profil) {
    return await apiRequest("/profil", {method: "PUT", headers: {"Content-Type": "application/json"}, body: JSON.stringify(profil)});
}