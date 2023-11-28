
const dateActuelle = new Date().toISOString().split('T')[0];

var mindate = document.getElementById("start-date");

mindate.min = dateActuelle;

mindate.onchange = function() {
    if (this.value > document.getElementById("end-date").value) {
        document.getElementById("end-date").value = this.value;
    }
    document.getElementById("end-date").min = this.value;
}
