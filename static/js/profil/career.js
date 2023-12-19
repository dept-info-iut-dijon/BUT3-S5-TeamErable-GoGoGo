htmx.config.useTemplateFragments = true;
document.querySelector("#search-input-historic").addEventListener('keyup', function(event) {
    var formData = new FormData();
    formData.append('game_name', event.target.value);

    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    var request = new XMLHttpRequest();
    request.open('POST', '/search-games-historic');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = function() {
        if (request.status == 200) {
            document.querySelector("#games-historic-list").innerHTML = request.responseText;
            htmx.process(document.querySelector("#games-historic-list"));
        }
    }
    request.send(formData);
});


document.getElementById('importForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('/import_JSON/', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            console.log('Réponse du serveur :', data);
        })
        .catch(error => {
            console.error('Erreur lors de la requête :', error);
        });
});



function importGame() {
    var fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.json';

    // Ajoutez un événement onchange pour déclencher l'envoi du fichier une fois sélectionné
    fileInput.addEventListener('change', function () {
        uploadFile(fileInput.files[0]);
    });

    // Cliquez sur le champ de fichier virtuel
    fileInput.click();
}

function uploadFile(file) {
    var formData = new FormData();
    let csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    formData.append('json_file', file);

    // Effectuez une requête Ajax vers le serveur avec le fichier
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/import-JSON', true);
    xhr.setRequestHeader('X-CSRFToken', csrf_token);
    xhr.onload = function () {
        if (xhr.status === 200) {
            // Succès de la requête, effectuez des actions supplémentaires si nécessaire
            notify(xhr.responseText);
        } else {
            // Gestion des erreurs
            notify(xhr.responseText);
        }
    };

    // Envoyez la requête avec le formulaire de données contenant le fichier
    xhr.send(formData);
}