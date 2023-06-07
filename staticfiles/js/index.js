var ctx = document.getElementById('myChart1');
load();
$.ajax({
    url: '/report/month/',
    type: "GET",
    data: {
        'select': "default",
    },
    success: function (data) {
        unload();

        new Chart(ctx, {
            type: "line",
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: data.label,
                        data: data.data,
                        lineTension: 0.2,
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
});

var ctx2 = document.getElementById('myChart2');
$.ajax({
    url: '/report/expire/',
    type: "GET",
    data: {
        'select': "default",
    },
    success: function (data) {
        unload();

        new Chart(ctx2, {
            type: "line",
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: data.label,
                        data: data.data,
                        lineTension: 0.2,
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
});

