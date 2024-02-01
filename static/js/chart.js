let endpoint = '/api/chart';

$.ajax({
    method: "POST",
    url: endpoint,
    data: {"type": document.getElementById("charts").value},
    success: function (data) {
        drawLineGraph(data, 'Chatline');
    },
    error: function (error_data) {
        console.log(error_data);
    }
})


function drawLineGraph(data, id) {
    let labels = data.labels;
    // let chartLabel = data.chartLabel;
    let chartdata = data.chartdata;
    let ctx = document.getElementById(id).getContext('2d');
    let myCharts = window.myCharts;
    if (myCharts !== undefined) {
        myCharts.destroy();
    }
    window.myCharts = new Chart(ctx, {
        type: 'line',

        // The data for our dataset
        data: {
            labels: labels,
            datasets: [{
                backgroundColor: 'rgb(255,201,85)',
                // borderColor: 'rgb(132,102,13)',

                data: chartdata,
            }]
        },

        // Configuration options
        options: {
            elements: {
                point: {
                    radius: 0
                }
            },
            legend: {
                display: false
            },
            scales: {
                xAxes: [{
                    values: "0:35:7",
                    display: true,
                    gridLines: {
                        display: false,
                    },

                }],
                yAxes: [{
                    values: "0:35:7",
                    position: 'right',
                    ticks: {
                        beginAtZero: false
                    },
                    gridLines: {
                        display: false,
                    }
                }]
            }
        }

    });
}


$("#charts").change(function () {
    let endpoint = '/api/chart';
    $.ajax({
        method: "POST",
        url: endpoint,
        data: {"type": document.getElementById("charts").value},
        success: function (data) {
            drawLineGraph(data, 'Chatline');
            console.log("update_drawing");
        },
        error: function (error_data) {
            console.log(error_data);
        }
    })
});