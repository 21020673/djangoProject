var tabs = document.querySelectorAll(".tab");
tabs.forEach(tab => {
    tab.addEventListener("click", function () {
        tabs.forEach(tab => {
            tab.classList.remove("tab-active");
        })
        this.classList.add("tab-active");
    })
})