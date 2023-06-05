var ctx_report = document.getElementById('myChart');
var url = "/report/month/";
$.ajax({
    url: url,
    type: "GET",
    data: {
        'select': select.val(),
    },
    success: function (data) {
        myChart = new Chart(ctx_report, {
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

var tabs = document.querySelectorAll(".tab");
tabs.forEach(tab => {
    tab.addEventListener("click", function () {
        tabs.forEach(tab => {
            tab.classList.remove("tab-active");
        })
        this.classList.add("tab-active");
        url = this.value;
        getdata()
        if (tab.textContent === "Month") {
            $("#predict").attr("disabled", false);
        } else {
            $("#predict").attr("disabled", true);
        }
    })
})

function getdata() {
    tabs.forEach(tab => {
        tab.disabled = true;
    })
    $.ajax({
        url: url,
        type: "GET",
        data: {
            'select': select.val(),
        },
        success: function (data) {
            myChart.data.labels = data.labels;
            myChart.data.datasets = [];
            myChart.data.datasets.push({
                label: data.label,
                data: data.data,
                lineTension: 0.2,
            })
            myChart.update();
            tabs.forEach(tab => {
                tab.disabled = false;
            })
        }
    });
}

select.change(function () {
    getdata()
    if ($('.tab-active').text() === 'Month') {
        $("#predict").attr("disabled", false);
    } else {
        $("#predict").attr("disabled", true);
    }
});

function predict() {
    tabs.forEach(tab => {
        tab.disabled = true;
    })
    $.ajax({
        url: "/predict/",
        type: "GET",
        data: {
            'select': select.val(),
        },
        success: function (data) {
            myChart.data.labels = data.labels;
            myChart.data.datasets.push({
                label: 'Prediction',
                data: data.data,
                lineTension: 0.2,
                borderColor: '#FF6384',
                backgroundColor: '#FFB1C1',
            })
            myChart.update();
            tabs.forEach(tab => {
                tab.disabled = false;
            })
        }
    });
    $("#predict").attr("disabled", true);
}
