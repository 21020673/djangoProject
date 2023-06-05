var navbar_tabs = document.querySelectorAll(".navbar-tab");
navbar_tabs.forEach(tab => {
    tab.addEventListener("click", function () {
        navbar_tabs.forEach(tab => {
            tab.classList.remove("font-semibold");
        })
        this.classList.add("font-semibold");
    })
})