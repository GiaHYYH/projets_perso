import { apiRequest } from "./client";

export function lireEvenements() {
    return apiRequest("/evenements");
}

export function creerEvenement(evenement) {
    return apiRequest("/evenements", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(evenement)
    });
}

export function modifierEvenement(evtId, evenement) {
    return apiRequest(`/evenements/${evtId}`, {method: "PUT", headers: {"Content-Type": "application/json"}, body: JSON.stringify(evenement)});
}

export function supprimerEvenement(evtId) {
    return apiRequest(`/evenements/${evtId}`, {method: "DELETE"});
}