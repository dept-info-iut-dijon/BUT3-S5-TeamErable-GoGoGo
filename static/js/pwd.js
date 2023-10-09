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

function validateForm() {
    var ret = checkSame() && checkLength();
    if (!ret) {
        alert('Le mot de passe doit être de 8 caractères minimum et les deux mots de passe doivent être identiques.');
    }
    return ret;
}

checkLength();
