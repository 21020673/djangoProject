function load() {
    let loading = document.getElementById('loading-circle');
    setTimeout(() => {
            loading.style.visibility = 'visible';
        }, 300);
}

function unload() {
    let loading = document.getElementById('loading-circle');
    loading.style.visibility = 'hidden';
}
