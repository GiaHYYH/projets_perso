export function afficherDuree(minutes) {

    if (minutes === null || minutes === undefined) {
        return "";
    }

    const heures = Math.floor(minutes / 60);
    const minutesRestantes = minutes % 60;

    if (heures === 0) {
        return `${minutesRestantes} minute${minutesRestantes > 1 ? "s" : ""}`;
    }

    if (minutesRestantes === 0) {
        return `${heures} heure${heures > 1 ? "s" : ""}`;
    }

    return `${heures} h ${minutesRestantes}`;

}