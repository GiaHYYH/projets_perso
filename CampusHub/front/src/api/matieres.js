import { apiRequest } from "./client";

export async function lireMatieres() {
    return await apiRequest("/matieres");
}

export async function creerMatiere(matiere) {
    return await apiRequest("/matieres", {method: "POST", body: JSON.stringify(matiere)});
}

export async function supprimerMatiere(mat_id) {
    return await apiRequest(`/matieres/${mat_id}`, {method: "DELETE"});
}

export async function modifierMatiere(mat_id, matiere) {
    return await apiRequest(`/matieres/${mat_id}`, {method: "PUT", body: JSON.stringify(matiere)});
}