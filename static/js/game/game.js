
document.querySelectorAll(".stone").forEach((element) => {
    element.addEventListener("click", () => {
        play(element);
    });
});

const board = document.querySelector(".board");

function play(element) {
    if (board.classList.contains("can-play")) {
        console.log("play", element.attributes.x, element.attributes.y);
        board.classList.remove("can-play");

        var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        var formData = new FormData();
        formData.append("id", document.querySelector("#game-id").value);
        formData.append("x", element.attributes.x.value);
        formData.append("y", element.attributes.y.value);

        request = new XMLHttpRequest();
        request.open("POST", "/game-play");
        request.setRequestHeader("X-CSRFToken", csrf_token);
        request.onload = function() {
            if (request.status == 200) {
                console.log(request.response);
            } else {
                document.querySelector(".notify").innerHTML = request.responseText;
                board.classList.add("can-play");
            }
        };
        request.send(formData);
    }
}
