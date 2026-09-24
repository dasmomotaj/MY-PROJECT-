
/* =========================================
   MOBILE MENU
========================================= */

function toggleMenu() {

    const menu = document.getElementById("navMenu");
    const button = document.querySelector(".menu-btn");

    if (!menu) return;

    const isOpen = menu.classList.toggle("show");

    if (button) {
        button.setAttribute(
            "aria-expanded",
            isOpen ? "true" : "false"
        );

        button.textContent = isOpen ? "✕" : "☰";
    }
}


/* =========================================
   DARK / LIGHT THEME
========================================= */

function updateThemeButton() {

    const button = document.querySelector(".theme-btn");

    if (!button) return;

    if (document.body.classList.contains("light")) {

        button.textContent = "☀️";
        button.setAttribute(
            "aria-label",
            "Switch to dark mode"
        );

    } else {

        button.textContent = "🌙";
        button.setAttribute(
            "aria-label",
            "Switch to light mode"
        );
    }
}


function toggleTheme() {

    document.body.classList.toggle("light");

    const isLight =
        document.body.classList.contains("light");

    localStorage.setItem(
        "theme",
        isLight ? "light" : "dark"
    );

    updateThemeButton();
}


/* =========================================
   PAGE LOAD
========================================= */

window.addEventListener(
    "DOMContentLoaded",
    function () {

        const savedTheme =
            localStorage.getItem("theme");

        if (savedTheme === "light") {
            document.body.classList.add("light");
        }

        updateThemeButton();
    }
);


/* =========================================
   CLOSE MOBILE MENU AFTER CLICK
========================================= */

document.addEventListener(
    "click",
    function (event) {

        const menu =
            document.getElementById("navMenu");

        const button =
            document.querySelector(".menu-btn");

        if (!menu || !button) return;

        if (
            menu.classList.contains("show") &&
            !menu.contains(event.target) &&
            !button.contains(event.target)
        ) {

            menu.classList.remove("show");

            button.setAttribute(
                "aria-expanded",
                "false"
            );

            button.textContent = "☰";
        }
    }
);

