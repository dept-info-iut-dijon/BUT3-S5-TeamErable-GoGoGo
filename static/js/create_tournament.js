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
