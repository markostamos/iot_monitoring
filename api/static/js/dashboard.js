/* globals Chart:false, feather:false */


$(document).ready(function() {

    feather.replace({ 'aria-hidden': 'true' })


    lower_bound = 0;
    upper_bound = Infinity;
    //Create empty charts
    var mychart = make_chart(id = "myChart", title = "");


    var real_time = false;
    var active = null;


    $("#get_temp_data").click(() => {
        [lower_bound, upper_bound] = get_upper_lower_bound();
        active = "temp";
        real_time = false;
        $("#get_temp_data").addClass('active');
        $("#get_humidity_data").removeClass('active');
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
        active = "humidity";
        $("#real_time").removeClass('active');

        $("#get_humidity_data").addClass('active');
        $("#get_temp_data").removeClass('active');

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
    $("#delete_notifications").click(() => {
        $.post('/delete_notifications', {
            device: chosen_device,
            building: chosen_building
        }, (res) => {
            $("#notification_body").empty();
        })

    });
    $(".dropdown-menu li a").click(function() {

        $("#timespan").text($(this).text());
        real_time = false;
        $("#real_time").removeClass('active');
        [lower_bound, upper_bound] = get_upper_lower_bound();
        $.post('/get_' + active + '_data', {
            username: "{{session['username']}}",
            device_name: chosen_device,
            upper_bound: parseInt(upper_bound),
            lower_bound: parseInt(lower_bound)
        }, (res) => {
            console.log(res);
            console.log(upper_bound);
            console.log(lower_bound);
            mychart.options.plugins.title.text = active == "temp" ? "Temperature (C)" : "Humidity (%)"
            draw_data(mychart, res["timestamps"], res["values"]);

        });



    });

    $("#delete_data").click(() => {

        $.post('/delete_data', {
            username: "{{session['username']}}",
            device_name: chosen_device,
            upper_bound: parseInt(upper_bound),
            lower_bound: parseInt(lower_bound),
            type: active ? active : "ALL"

        }, (res) => {
            console.log(res);
            draw_data(mychart, [], []);
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
                for (i = 0; i < res["timestamps"].length; i++) {
                    console.log("works");
                    console.log(res["values"][i]);
                    addData(mychart, res["timestamps"][i], res["values"][i]);
                }

            });
            lower_bound = new Date();
        }

        $.post('/get_notifications', {
            username: "{{session['username']}}",
            device: chosen_device,
            building: chosen_building
        }, (res) => {
            $("#notification_body").empty();
            if (chosen_device == "None" && chosen_building == "None") {
                console.log("none");

                for (i = 0; i < res.notifications.length; i++) {
                    notification = res.notifications[i];

                    $("#notification_body").append(
                        `<tr id="${notification["id"]}">
                    <td class="text-center">${notification["date"]}</td>
                    <td class="text-center">${notification["severity"]}</td>
                    <td class="text-center">${notification["building"]}</td>
                    <td class="text-center">${notification["device"]}</td>
                    <td class="text-center">${notification["text"]}</td>
                    <td class="text-center">
                    <button type="button" onclick="delete_notification(this)" class="btn btn-danger btn-sm">X</button>
                    </td>
                    </tr>`
                    )
                }
            } else if (chosen_device == "None") {
                for (i = 0; i < res.notifications.length; i++) {
                    notification = res.notifications[i];

                    $("#notification_body").append(
                        `<tr id="${notification["id"]}">
                    <td class="text-center">${notification["date"]}</td>
                    <td class="text-center">${notification["severity"]}</td>
                    <td class="text-center">${notification["device"]}</td>
                    <td class="text-center">${notification["text"]}</td>
                    <td class="text-center">
                    <button type="button" onclick="delete_notification(this)" class="btn btn-danger btn-sm">X</button>
                    </td>
                    </tr>`
                    )
                }
            } else {
                for (i = 0; i < res.notifications.length; i++) {
                    notification = res.notifications[i];

                    $("#notification_body").append(
                        `<tr id="${notification["id"]}">
                    <td class="text-center">${notification["date"]}</td>
                    <td class="text-center">${notification["severity"]}</td>
                    <td class="text-center">${notification["text"]}</td>
                    <td class="text-center">
                    <button type="button" onclick="delete_notification(this)" class="btn btn-danger btn-sm">X</button>
                    </td>
                    </tr>`
                    )
                }
            }


        })


    }, 2000);

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
        return [0, now.getTime()];

    } else if (value == "Last Minute") {
        lower_bound.setMinutes(now.getMinutes() - 1);

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

    chart.data.datasets[0].data.push(data);
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