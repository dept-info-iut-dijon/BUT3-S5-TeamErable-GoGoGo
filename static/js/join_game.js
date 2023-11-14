document.querySelector("#search-input").addEventListener('keyup', async function(event) {
    var formData = new FormData();
    formData.append('game_name', event.target.value);

    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    await fetch('/search-game', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token
        },
        body: formData
    })
    .then(async function(response) {
        if (response.status == 200) {
            document.querySelector("#game-list").innerHTML = await response.text();
            htmx.process(document.querySelector("#game-list"));
        }
    })
});

document.querySelectorAll(".pass-to-next").forEach(function(element) {
    element.addEventListener('paste', function(event) {
        var pastedText = event.clipboardData.getData('text');
        var input = event.target;

        for (var i = 0; i < pastedText.length; i++) {
            while (input.value.length == 4) {
                var newinput = input.nextElementSibling.nextElementSibling;
                if (newinput.type == "text") {
                    input = newinput;
                    input.focus();
                }
                else break;
            }
            if (input.type != "text") break;
            if (input.value.length == 4) break;
            input.value += pastedText[i];
        }
        event.preventDefault();
    });

    element.addEventListener('keyup', function(event) {
        event.target.value = event.target.value.toUpperCase();
        event.target.value = event.target.value.replace(/[^A-Z0-9]/g, '');

        if (event.target.value.length == 4) {
            event.target.nextElementSibling.nextElementSibling.focus();
        }
    })
});

document.querySelector(".pass-to-next-last").addEventListener('keyup', function(event) {
    event.target.value = event.target.value.toUpperCase();
    event.target.value = event.target.value.replace(/[^A-Z0-9]/g, '');
});

document.querySelector("form#join-by-code").addEventListener('submit', async function(event) {
    event.target.querySelector("input[type='submit']").disabled = true;
    event.preventDefault();

    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    var formData = new FormData(event.target);
    formData.append(
        'code',
        event.target.querySelector("#search-code-input-0").value +
        event.target.querySelector("#search-code-input-1").value +
        event.target.querySelector("#search-code-input-2").value +
        event.target.querySelector("#search-code-input-3").value
    );

    await fetch('/game-code', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token
        },
        redirect: 'follow',
        body: formData
    })
    .then(async function(response) {
        if (response.redirected) {
            window.location.replace(response.url);
        }
        else {
            document.querySelector(".notify").innerHTML = await response.text();
            event.target.querySelector("input[type='submit']").disabled = false;
        }
    });
});
