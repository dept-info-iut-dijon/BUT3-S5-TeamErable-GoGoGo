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