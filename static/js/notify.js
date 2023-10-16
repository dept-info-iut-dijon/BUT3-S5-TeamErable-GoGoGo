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
