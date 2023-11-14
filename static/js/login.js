async function validateForm() {
    document.querySelector('input[type="submit"]').disabled = true;

    var formData = new FormData();
    formData.append('username', document.getElementById('username').value);
    formData.append('password', document.getElementById('password').value);

    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    await fetch('/login', {
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
            document.querySelector('input[type="submit"]').disabled = false;
        }
    });

    return false;
}
