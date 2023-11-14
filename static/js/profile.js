async function readURL(input) {
    if (input.files && input.files[0]) {
        var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        var formData = new FormData();
        formData.append('pfp', input.files[0]);

        await fetch('/change-pfp', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token
            },
            body: formData
        })
        .then(async function(response) {
            document.querySelector(".notify").innerHTML = await response.text();

            if (response.status == 200) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    document.querySelector('.profile-pic').setAttribute('src', e.target.result);
                }
                reader.readAsDataURL(input.files[0]);
            }
        });
    }
}

document.querySelector(".file-upload").addEventListener('change', function(){
    readURL(this);
});

document.querySelector(".upload-button").addEventListener('click', function() {
    document.querySelector(".file-upload").click();
});



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



document.querySelector("#change-pwd").addEventListener('submit', async function(event) {
    event.preventDefault();
    document.querySelector('form#change-pwd input[type="submit"]').disabled = true;

    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    var formData = new FormData();
    formData.append('old-pwd', document.querySelector('input[name="old-pwd"]').value);
    formData.append('new-pwd', document.querySelector('input[name="new-pwd"]').value);
    formData.append('new-pwd-confirm', document.querySelector('input[name="new-pwd-confirm"]').value);

    await fetch('/change-pwd', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token
        },
        body: formData
    })
    .then(async function(response) {
        document.querySelector(".notify").innerHTML = await response.text();

        if (response.status == 200) {
            setTimeout(function() {
                window.location.reload();
            }, 1000);
        } else {
            document.querySelector('form#change-pwd input[type="submit"]').disabled = false;
        }
    });
});




document.querySelector("#search-input").addEventListener('keyup', async function(event) {
    var formData = new FormData();
    formData.append('username', event.target.value);

    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    await fetch('/search-notfriend-user', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token
        },
        body: formData
    })
    .then(async function(response) {
        if (response.status == 200) {
            document.querySelector("#user-datalist").innerHTML = await response.text();
            htmx.process(document.querySelector("#user-datalist"));
        }
    })
});



document.body.addEventListener("htmx:afterRequest", async function(event) {
    setTimeout(async function() {
        if (
            !(
                (event.detail.xhr.responseURL.startsWith(window.location.origin + "/add-friend")) ||
                (event.detail.xhr.responseURL.startsWith(window.location.origin + "/delete-friend"))
            )
        ) return;
        document.querySelector(".notify").innerHTML = event.detail.xhr.responseText;

        document.querySelector("#search-input").dispatchEvent(new KeyboardEvent('keyup', {key: 'a'}));

        var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        await fetch('/friend-list', {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrf_token
            }
        })
        .then(async function(response) {
            if (response.status == 200) {
                document.querySelector("#friends-list").innerHTML = await response.text();
                htmx.process(document.querySelector("#friends-list"));
            }
        })
    }, 100);
});



document.querySelector("#delete-account").addEventListener('submit', async function(event) {
    event.preventDefault();
    document.querySelector('form#delete-account input[type="submit"]').disabled = true;

    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    var formData = new FormData();
    formData.append('password', document.querySelector('input[name="password"]').value);

    await fetch('/delete-account', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token
        },
        redirect: 'follow',
        body: formData
    })
    .then(async function(response) {
        document.querySelector(".notify").innerHTML = await response.text();

        if (response.redirected) {
            setTimeout(function() {
                window.location.href = response.url;
            }, 1000);
        }
        else {
            document.querySelector('form#delete-account input[type="submit"]').disabled = false;
        }
    });
});
