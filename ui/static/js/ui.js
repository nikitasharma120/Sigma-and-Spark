function openModal(index) {
    const modal = document.getElementById("modal" + index);
    if (modal) {
        modal.style.display = "flex";
    }
}

function closeModal(index) {
    const modal = document.getElementById("modal" + index);
    if (modal) {
        modal.style.display = "none";
    }
}

/* Close modal when clicking outside content */
window.onclick = function (event) {
    if (event.target.classList.contains("modal")) {
        event.target.style.display = "none";
    }
};
