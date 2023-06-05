const container = document.querySelector("html");
const switcher_navbar = document.getElementById("dark-mode-navbar");
const switcher_sidebar = document.getElementById("dark-mode-navbar");
if (localStorage.getItem("data-theme")) {
    container.setAttribute("data-theme", localStorage.getItem("data-theme"));
    darken(1)
}

function darken(r) {
    let dataTheme = container.getAttribute("data-theme");
    let theme_switch;

    if (dataTheme === "light") {
        theme_switch = 1
    } else {
        theme_switch = 0
    }
    if (r) {
        theme_switch = !theme_switch
    } //so the oppisite of the theme stored is used when calling this function
    if (theme_switch) {
        container.setAttribute("data-theme", "dark");
        localStorage.setItem("data-theme", "dark");
        switcher_navbar.checked = true;
        switcher_sidebar.checked = true;
    } else {
        container.setAttribute("data-theme", "light");
        localStorage.setItem("data-theme", "light");
        switcher_navbar.checked = false;
        switcher_sidebar.checked = false;
    }
}