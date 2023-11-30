
const base_url = window.location.hostname + ":" + window.location.port + "/";
const game_id = document.querySelector("#game-id").value;
const websocket = new WebSocket("ws://" + base_url + "game/" + game_id + "/");



websocket.onopen = function(event) {
    websocket.send(JSON.stringify({
        'type': 'connect',
        'data': 'hello server'
    }));
}

websocket.onclose = function(event) {
    websocket.send(JSON.stringify({
        'type': 'disconnect',
        'data': 'bye server'
    }));
}

websocket.onmessage = function(event) {
    let raw_data = JSON.parse(event.data);
    let type = raw_data.type;
    let data = raw_data.data;

    switch(type) {
        case 'connect':
            receivedConnect(data);
            break;

        case 'disconnect':
            break; // Ne fait rien pour l'instant, mais on pourrait afficher une notification

        case 'play':
            receivedPlay(data);
            break;

        case 'can-play':
            receivedCanPlay(data);
            break;

        case 'eaten-tiles':
            receivedEatenTiles(data);
            break;

        case 'end-game':
            receivedEndGame(data);
            break;

        case 'error':
            notify('<p class="error">' + data + '</p>');
            break;

        default:
            console.log("unknown message type: ", type);
            break;
    }
}

function receivedConnect(data) {
    let user_id = data.id;
    let color = data.color;

    let formData = new FormData();
    formData.append("game-id", game_id);
    formData.append("user-id", user_id);
    
    let csrf_token = document.querySelector("input[name=csrfmiddlewaretoken]").value;

    var request = new XMLHttpRequest();
    request.open('POST', '/game-view-player');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = function() {
        if (request.status === 200) {
            document.querySelector("#container-" + color + "-player").innerHTML = request.responseText;
        }
        else {
            console.log("error: ", request.responseText);
        }
    }
    request.send(formData);
}

function parseReceivedPlayData(stringData, callback) {
    let list = stringData.split("\n");
    for (let i = 0; i < list.length; i++) {
        if (list[i] === "") continue;

        let coords = list[i].split(";");
        let x = parseInt(coords[0]);
        let y = parseInt(coords[1]);

        callback(x, y);
    }
}

function receivedPlay(data) {
    let changes = JSON.parse(data);

    let rm = changes.r;
    let white = changes.w;
    let black = changes.b;

    parseReceivedPlayData(rm, (x, y) => {
        let stone = document.querySelector(`.stone[x="${x}"][y="${y}"]`);

        if (stone.classList.contains("white")) {
            stone.classList.remove("white");
        }
        else if (stone.classList.contains("black")) {
            stone.classList.remove("black");
        }
    });

    parseReceivedPlayData(white, (x, y) => {
        let stone = document.querySelector(`.stone[x="${x}"][y="${y}"]`);
        stone.classList.add("white");
    });

    parseReceivedPlayData(black, (x, y) => {
        let stone = document.querySelector(`.stone[x="${x}"][y="${y}"]`);
        stone.classList.add("black");
    });
}

function receivedCanPlay(data) {
    if (data === true) {
        board.classList.add("can-play");
        action_buttons.classList.remove("hidden");
    }
    else {
        board.classList.remove("can-play");
        action_buttons.classList.add("hidden");
    }
}

function receivedEatenTiles(data) {
    let eaten = JSON.parse(data);

    let score_white = document.querySelector(".score.white");
    let score_black = document.querySelector(".score.black");

    score_white.innerHTML = eaten.w;
    score_black.innerHTML = eaten.b;
}

function receivedEndGame(data) {
    let parsed_data = JSON.parse(data);

    let winner = parsed_data.winner;
    let points = parsed_data.points;

    let end_game_modal = document.querySelector(".band");

    let winner_text = end_game_modal.querySelector("#band-big-text");
    let points_text = end_game_modal.querySelector("#band-small-text");

    if (winner === "w") {
        winner_text.innerHTML = `Les blancs (${points[winner].username}) ont gagné la partie !`;
        points_text.innerHTML = `${points.w.count} (${points.w.username}) vs ${points.b.count} (${points.b.username})`;
    }
    else if (winner === "b") {
        winner_text.innerHTML = `Les noirs (${points[winner].username}) ont gagné la partie !`;
        points_text.innerHTML = `${points.b.count} (${points.b.username}) vs ${points.w.count} (${points.w.username})`;
    }
    else {
        winner_text.innerHTML = "Égalité !";
        points_text.innerHTML = `${points.w.count} (${points.w.username}) vs ${points.b.count} (${points.b.username})`;
    }

    end_game_modal.classList.remove("hidden");
}



document.querySelectorAll(".stone").forEach((element) => {
    element.addEventListener("click", () => {
        play(element);
    });
});

const board = document.querySelector(".board");
const action_buttons = document.querySelector("#action-buttons");

function play(element) {
    if (board.classList.contains("can-play")) {
        websocket.send(JSON.stringify({
            'type': 'play',
            'data': element.attributes.x.value + ";" + element.attributes.y.value
        }));
    }
}

function skip() {
    websocket.send(JSON.stringify({
        'type': 'skip',
        'data': null
    }));
}

function giveUp() {
    websocket.send(JSON.stringify({
        'type': 'give-up',
        'data': null
    }));
}

document.querySelector("#skip-button").addEventListener("click", skip);
document.querySelector("#give-up-button").addEventListener("click", giveUp);



const code = document.querySelector("#code");

function toggleCodeVisibility() {
    let checked = document.querySelector("#show-code").querySelector("input[type=checkbox]").checked;
    if (checked) code.classList.remove("opacity-0");
    else code.classList.add("opacity-0");
}