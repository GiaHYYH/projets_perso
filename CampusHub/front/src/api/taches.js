import { apiRequest } from "./client";

export async function lireTaches() {
    return await apiRequest("/taches");
}

export async function creerTache(tache) {
    return await apiRequest("/taches", {method: "POST", body: JSON.stringify(tache)});
}

export async function supprimerTache(tac_id) {
    return await apiRequest(`/taches/${tac_id}`, {method: "DELETE"});
}

export async function lireMatieresTache(tac_id) {
    return await apiRequest(`/taches/${tac_id}/matieres`);
}

export async function lierTacheMatiere(tac_id, mat_id) {
    return await apiRequest(`/taches/${tac_id}/matieres/${mat_id}`, {method: "POST"});
}

export async function supprimerLienTacheMatiere(tac_id, mat_id) {
    return await apiRequest(`/taches/${tac_id}/matieres/${mat_id}`, {method: "DELETE"});
}

export async function modifierStatutTache(tac_id, statut) {
    return await apiRequest(`/taches/${tac_id}/statut`, {method: "PATCH", body: JSON.stringify({tac_status: statut})});
}

export async function modifierTache(id, donnees) {
    return await apiRequest(`/taches/${id}`, {method: "PUT", headers: {"Content-Type": "application/json"}, body: JSON.stringify(donnees)});
}