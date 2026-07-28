export function afficherDate(date) {
    if (!date) {
        return "Aucune";
    }
    return new Date(date).toLocaleDateString("fr-FR");
}