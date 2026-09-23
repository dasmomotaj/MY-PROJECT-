
function toggleMenu() {
    const menu = document.getElementById("navMenu");
    if (menu) {
        menu.classList.toggle("show");
    }
}

function toggleTheme() {
    document.body.classList.toggle("light");

    if (document.body.classList.contains("light")) {
        localStorage.setItem("theme", "light");
    } else {
        localStorage.setItem("theme", "dark");
    }
}

function searchCards(inputId, cardClass) {
    const input = document.getElementById(inputId);
    const cards = document.getElementsByClassName(cardClass);

    if (!input) return;

    const query = input.value.toLowerCase();

    for (let card of cards) {
        const text = card.innerText.toLowerCase();

        if (text.includes(query)) {
            card.style.display = "";
        } else {
            card.style.display = "none";
        }
    }
}

window.addEventListener("DOMContentLoaded", function() {
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "light") {
        document.body.classList.add("light");
    }
});
