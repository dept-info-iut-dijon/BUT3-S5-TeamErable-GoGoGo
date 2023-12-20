const play_button = document.querySelector("#play");
const pause_button = document.querySelector("#pause");
const duration_time = document.querySelector("#duration-time");
const duration_slider = document.querySelector("#duration-slider");
const color = document.querySelector("#color").value;

let pause = true;

play_button.addEventListener("click", () => {
    play_button.classList.add("hidden");
    pause_button.classList.remove("hidden");
    pause = false;
});

pause_button.addEventListener("click", () => {
    pause_button.classList.add("hidden");
    play_button.classList.remove("hidden");
    pause = true;
});
