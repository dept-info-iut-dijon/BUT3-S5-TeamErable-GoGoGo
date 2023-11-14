var checkSame = function() {
    if ((document.getElementById('password').value == document.getElementById('confirm-password').value) && document.getElementById('password').value != '') {
        document.getElementById('password-same-check').style.color = 'green';
        document.getElementById('password-same-check').innerHTML = '✔';
        return true;
    }
    else if (document.getElementById('confirm-password').value == '') {
        document.getElementById('password-same-check').innerHTML = '';
    }
    else {
        document.getElementById('password-same-check').style.color = 'red';
        document.getElementById('password-same-check').innerHTML = '✖';
    }
    return false;
}

var checkLength = function() {
    if (document.getElementById('password').value.length >= 8) {
        document.getElementById('password-length-check').style.color = 'green';
        document.getElementById('password-length-check').innerHTML = '✔';
        return true;
    }
    else {
        document.getElementById('password-length-check').style.color = 'red';
        document.getElementById('password-length-check').innerHTML = '✖';
    }
    return false;
}

var check = function() {
    checkSame();
    checkLength();
}

async function validateForm() {
    if (!checkLength()) {
        document.querySelector(".notify").innerHTML = '<p class="error">Le mot de passe doit être de 8 caractères minimum.</p>';
        return false;
    }

    if (!checkSame()) {
        document.querySelector(".notify").innerHTML = '<p class="error">Les mots de passe ne correspondent pas.</p>';
        return false;
    }

    document.querySelector('input[type="submit"]').disabled = true;

    var formData = new FormData();
    formData.append('username', document.getElementById('username').value);
    formData.append('email', document.getElementById('email').value);
    formData.append('password1', document.getElementById('password').value);
    formData.append('password2', document.getElementById('confirm-password').value);

    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    await fetch('/register', {
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

checkLength();
