export function afficherPriorite(priorite) {

    if (priorite === 'H') {
        return "Haute";
    } else if (priorite === 'M') {
        return "Moyenne";
    } else {
        return "Basse";
    }

}