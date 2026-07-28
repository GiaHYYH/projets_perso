import { apiRequest } from "./client";


export async function lireDashboard() {
    return await apiRequest("/dashboard");
}


export async function lireRetardsDashboard() {
    return await apiRequest("/dashboard/retards");
}


export async function lireUrgentesDashboard() {
    return await apiRequest("/dashboard/urgentes");
}