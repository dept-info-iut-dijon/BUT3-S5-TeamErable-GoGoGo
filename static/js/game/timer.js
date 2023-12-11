/**
 * Récupérer l'élément par son ID
 * @param {string} color Couleur du joueur
 * @returns {boolean} Si on a plus de temps
 */
function getTimerElement(color) {
    // Récupérer l'élément par son ID
    var countdownElement = document.querySelector("#timer-" + color);
    return updateCountdown(countdownElement);
}


/**
 * Met à jour le temps
 * @param {HTMLElement} countdownElement Elemennt du temps
 */
function updateCountdown(countdownElement) {
    // Récupérer la valeur du temps actuel au format "hh:mm:ss"
    var currentTime = countdownElement.innerText;
    var timeArray = currentTime.split(":");
    var hours = parseInt(timeArray[0], 10);
    var minutes = parseInt(timeArray[1], 10);
    var seconds = parseInt(timeArray[2], 10);

    // Décrémenter d'une seconde
    if (seconds > 0) {
        seconds--;
    } else {
        if (minutes > 0) {
            minutes--;
            seconds = 59;
        } else {
            if (hours > 0) {
                hours--;
                minutes = 59;
                seconds = 59;
            }
        }
    }

    // Mettre à jour l'élément avec la nouvelle valeur
    countdownElement.innerText = formatTime(hours) + ":" + formatTime(minutes) + ":" + formatTime(seconds);

    return seconds <= 0 && minutes <= 0 && hours <= 0;
}

/**
 * Formater le temps
 * @param {number} time Le chiffre à formater
 * @returns {string} Le temps avec un 0 devant le chiffre
 */
function formatTime(time) {
    return time < 10 ? "0" + time : time;
}

// Exécuter la fonction updateCountdown toutes les secondes
setInterval( function() {
    if (!game_ended && has_second_player_element.value != "False") {
        let timed_out = getTimerElement(getCanPlay() ? player_color : getOpponentColor());
        if (timed_out) checkState();
    }
}, 1000);
