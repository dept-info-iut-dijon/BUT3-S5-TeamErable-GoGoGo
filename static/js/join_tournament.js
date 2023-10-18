htmx.config.useTemplateFragments = true;
document.querySelector("#search-input").addEventListener('keyup', function(event) {
    var formData = new FormData();
    formData.append('tournament_name', event.target.value);

    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    var request = new XMLHttpRequest();
    request.open('POST', '/search-tournament');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = function() {
        if (request.status == 200) {
            document.querySelector("#tournament-list").innerHTML = request.responseText;
            htmx.process(document.querySelector("#tournament-list"));
        }
    }
    request.send(formData);
});