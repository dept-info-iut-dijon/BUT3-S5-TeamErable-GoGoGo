document.body.addEventListener("htmx:afterRequest", function(event) {
    setTimeout(function() {
        if (
            !(
                (event.detail.xhr.responseURL.startsWith(window.location.origin + "/create-tournament"))
            )
        ) return;
        if (event.detail.xhr.status == 200) {
            setTimeout(function() {
                window.location.href = event.detail.xhr.responseText;
            }, 1000);
        }
        else {
            document.querySelector(".notify").innerHTML = event.detail.xhr.responseText;
        }
    });
});