document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("infoModal");
    const infoText = document.getElementById("infoText");
    const closeBtn = document.getElementsByClassName("close-btn")[0];

    infoText.onclick = function() {
        modal.style.display = "block";
    };

    closeBtn.onclick = function() {
        modal.style.display = "none";
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
});