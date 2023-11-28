document.body.addEventListener("htmx:afterRequest", function(event) {
    if (
        !(
            (event.detail.xhr.responseURL.startsWith(window.location.origin + "/create-tournament"))
        )
    ) return;
    document.querySelector('form input[type="submit"]').disabled = true;
    if (event.detail.xhr.status == 200) {
        setTimeout(function() {
            window.location.href = event.detail.xhr.responseText;
        }, 1000);
    }
    else {
        document.querySelector(".notify").innerHTML = event.detail.xhr.responseText;
        document.querySelector('form input[type="submit"]').disabled = false;
    }
});

// Récupérer la case à cocher et le div
var handicap = document.getElementById('handicap-form');

// Ajouter un écouteur d'événement pour la case à cocher
function toggleHandicap() {

    // Inverser l'état actif du switch button
    let switchbutton = document.getElementById('tournament-is-handicap').querySelector('input[type="checkbox"]');

    // Si le switch button est activé, afficher le div, sinon le masquer
    handicap.hidden = !switchbutton.checked;


};