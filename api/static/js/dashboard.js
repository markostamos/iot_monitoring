/* globals Chart:false, feather:false */


$(document).ready(function() {

    feather.replace({ 'aria-hidden': 'true' })



    //Create empty charts
    var mychart = make_chart(id = "myChart", title = "");


    var real_time = false;
    var active = "temp";


    $("#get_temp_data").click(() => {
        [lower_bound, upper_bound] = get_upper_lower_bound();
        active = "temp";
        real_time = false;

        $("#real_time").removeClass('active');
        $.post('/get_temp_data', {
            username: "{{session['username']}}",
            device_name: chosen_device,
            upper_bound: parseInt(upper_bound),
            lower_bound: parseInt(lower_bound)
        }, (res) => {
            mychart.options.plugins.title.text = "Temperature (C)";
            draw_data(mychart, res["timestamps"], res["values"]);

        })

    });

    $("#get_humidity_data").click(() => {

        [lower_bound, upper_bound] = get_upper_lower_bound();
        real_time = false;
        $("#real_time").removeClass('active');
        active = "humidity";
        $.post('/get_humidity_data', {
            username: "{{session['username']}}",
            device_name: chosen_device,
            upper_bound: parseInt(upper_bound),
            lower_bound: parseInt(lower_bound)
        }, (res) => {
            mychart.options.plugins.title.text = "Humidity (%)";
            draw_data(mychart, res["timestamps"], res["values"]);

        });
    })

    $("#real_time").click(() => {
        $("#real_time").button('toggle');
        real_time = !real_time;
        lower_bound = new Date();
    })

    setInterval(get_real_time_data = () => {
        if (real_time) {

            console.log(new Date().getTime());
            $.post('/get_' + active + '_data', {
                username: "{{session['username']}}",
                device_name: chosen_device,
                upper_bound: parseInt(new Date().getTime()),
                lower_bound: parseInt(lower_bound.getTime())
            }, (res) => {
                draw_data(mychart, res["timestamps"], res["values"]);

            });
        }
    }, 1000);

});



function get_upper_lower_bound() {
    var value = $("#timespan").text().trim();
    var now = new Date();
    lower_bound = new Date();
    if (value == "Last Hour") {

        lower_bound.setHours(now.getHours() - 1);

    } else if (value == "Last Day") {

        lower_bound.setHours(now.getHours() - 24);


    } else if (value == "Last Week") {

        lower_bound.setHours(now.getHours() - 24 * 7);

    } else if (value == "All time") {
        lower_bound = 0;

    } else if (value == "Real Time") {
        lower_bound = 0;

    }
    upper_bound = now;

    return [lower_bound.getTime(), upper_bound.getTime()];
}

function draw_data(chart, timestamps, values) {
    chart.data.labels = timestamps;
    chart.data.datasets[0].data = values;
    chart.update();
}







//Adds data point to chart
function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}



function removeData(chart) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}


function make_chart(id, title) {

    var chart = new Chart(document.getElementById(id), {
        type: 'line',
        data: {
            labels: [

            ],
            datasets: [{
                data: [],
                lineTension: 0,
                backgroundColor: 'transparent',
                borderColor: '#007bff',
                borderWidth: 4,
                pointBackgroundColor: '#007bff',
            }]
        },
        options: {
            responsive: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: title
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'minute',
                        format: "HH:MM:SS"
                    },
                    ticks: {
                        maxTicksLimit: 5
                    }
                }
            },
            legend: {
                display: false
            }

        }
    });
    return chart;
}