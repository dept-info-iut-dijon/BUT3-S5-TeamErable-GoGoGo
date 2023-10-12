function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            document.querySelector('.profile-pic').setAttribute('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);

        var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        var formData = new FormData();
        formData.append('pfp', input.files[0]);
        var request = new XMLHttpRequest();
        request.open('POST', '/change-pfp');
        request.setRequestHeader('X-CSRFToken', csrf_token);
        request.onload = function() {
            document.querySelector(".notify").innerHTML = request.responseText;
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