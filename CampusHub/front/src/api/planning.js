import { apiRequest } from "./client";

export async function recupererPlanningAutomatique() {
    return await apiRequest("planning/automatique");
}