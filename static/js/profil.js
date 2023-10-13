function readURL(input) {
    if (input.files && input.files[0]) {
        var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        var formData = new FormData();
        formData.append('pfp', input.files[0]);
        var request = new XMLHttpRequest();
        request.open('POST', '/change-pfp');
        request.setRequestHeader('X-CSRFToken', csrf_token);
        request.onload = function() {
            document.querySelector(".notify").innerHTML = request.responseText;

            if (request.status == 200) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    document.querySelector('.profile-pic').setAttribute('src', e.target.result);
                }
                reader.readAsDataURL(input.files[0]);
            }
        }
        request.send(formData);
    }
}

document.querySelector(".file-upload").addEventListener('change', function(){
    readURL(this);
});

document.querySelector(".upload-button").addEventListener('click', function() {
    document.querySelector(".file-upload").click();
});



document.querySelector(".notify").addEventListener('DOMSubtreeModified', function() {
    showNotification();
});

function showNotification() {
    var notifyElement = document.querySelector(".notify");
    if (notifyElement.innerHTML == "") return;
    notifyElement.classList.toggle("active");

    setTimeout(function(){
        notifyElement.classList.remove("active");
        
        setTimeout(function(){
            notifyElement.innerHTML = "";
        }, 200);

    }, 2000);
};



document.querySelectorAll(".sidebar-link").forEach(function(element) {
    element.addEventListener('click', function(event) {
        var links = document.querySelectorAll(".sidebar-link");
        links.forEach(element => {
            element.classList.remove("active");
        });
    
        var sections = document.querySelectorAll("section");
        sections.forEach(element => {
            element.classList.remove("active");
        });
    
        event.target.classList.toggle("active");
        document.querySelector(event.target.getAttribute("activate")).classList.toggle("active");
    });
});



document.querySelector("#change-pwd").addEventListener('submit', function(event) {
    event.preventDefault();
    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    var formData = new FormData();
    formData.append('old-pwd', document.querySelector('input[name="old-pwd"]').value);
    formData.append('new-pwd', document.querySelector('input[name="new-pwd"]').value);
    formData.append('new-pwd-confirm', document.querySelector('input[name="new-pwd-confirm"]').value);
    var request = new XMLHttpRequest();
    request.open('POST', '/change-pwd');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = function() {
        if (request.status == 400) {
            document.querySelector(".notify").innerHTML = request.responseText;
        } else if (request.status == 200) {
            document.querySelector(".notify").innerHTML = request.responseText;
            setTimeout(function() {
                window.location.reload();
            }, 1000);
        }
    }
    request.send(formData);
});




document.querySelector("#search-input").addEventListener('keyup', function(event) {
    var formData = new FormData();
    formData.append('username', event.target.value);

    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    var request = new XMLHttpRequest();
    request.open('POST', '/search-notfriend-user');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = function() {
        if (request.status == 200) {
            document.querySelector("#user-datalist").innerHTML = request.responseText;
            htmx.process(document.querySelector("#user-datalist"));
        }
    }
    request.send(formData);
});



document.body.addEventListener("htmx:configRequest", function(event) {
    setTimeout(function() {
        document.querySelector("#search-input").dispatchEvent(new KeyboardEvent('keyup', {key: 'a'}));
    }, 100);
});
