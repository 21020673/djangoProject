const switcher_navbar = document.getElementById("dark-mode-navbar");
const switcher_sidebar = document.getElementById("dark-mode-sidebar");

let dataTheme = container.getAttribute("data-theme");


if (dataTheme === "dark") {
    switcher_navbar.checked = true;
    switcher_sidebar.checked = true;
} else if (dataTheme === "light") {
    switcher_navbar.checked = false;
    switcher_sidebar.checked = false;
}