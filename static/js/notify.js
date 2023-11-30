function notify(message) {
    var notifyElement = document.querySelector(".notify ul");
    var notif = document.createElement("li");
    notifyElement.appendChild(notif);
    notif.innerHTML = message;
    while (notif.children.length > 1) { // Pour une raison inconnue, le innerHTML ajoute 2 enfants au lieu d'un seul
        notif.removeChild(notif.children[1]);
    }

    setTimeout(function(){
        notif.remove();
    }, 5000);
}
