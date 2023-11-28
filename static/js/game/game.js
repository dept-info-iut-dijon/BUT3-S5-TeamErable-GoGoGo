
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
        case 'disconnect':
            break; // Ne fait rien pour l'instant, mais on pourrait afficher une notification

        case 'play':
            receivedPlay(data);
            break;

        case 'can-play':
            receivedCanPlay(data);
            break;

        case 'error':
            document.querySelector(".notify").innerHTML = '<p class="error">' + data + '</p>';
            break;

        default:
            console.log("unknown message type: ", type);
            break;
    }
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
        stone.classList.remove("white");
        stone.classList.remove("black");
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