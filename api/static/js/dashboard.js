/* globals Chart:false, feather:false */



$(document).ready(function() {

    feather.replace({ 'aria-hidden': 'true' })



    //Create empty charts
    var mychart = make_chart(id = "myChart", title = "");
    /* var humidity_chart = make_chart(id = "humidity_chart", title = "Humidity %"); */

    var chart_type = "realtime";


    $("#get_temp_data").click(() => {

        $.post('/get_temp_data', {
            username: "{{session['username']}}",
            device_name: chosen_device
        }, (res) => {
            mychart.options.plugins.title.text = "Temperature (C)";
            draw_data(mychart, res["timestamps"], res["values"]);

        })


        //draw_data(mychart, [1644765567000, 1644766567000, 1644785567000], [1, 2, 3])

    })
    $("#get_humidity_data").click(() => {

        $.post('/get_humidity_data', {
            username: "{{session['username']}}",
            device_name: chosen_device
        }, (res) => {
            mychart.options.plugins.title.text = "Humidity (%)";
            draw_data(mychart, res["timestamps"], res["values"]);

        });



    })

    /* 
        //Connect via socket with sever
        var socket = io();
        socket.on('connect', function() {
            socket.emit('my_event', {
                data: 'I\'m connected!'
            });
            console.log("connected!")
        });

        //On every new mqtt message update values and charts
        socket.on("mqtt_message", function(msg, cb) {
            var a = 3;
            var temp = msg["payload"]["temperature"];
            var humidity = msg["payload"]["humidity"];
            var time = msg["payload"]["timestamp"];

            //Update values
            $("#temperature").text(temp);
            $("#humidity").text(humidity);

            tempList.push(temp);
            humidityList.push(humidity);
            timeList.push(time);
            if (chart_type == "realtime") {
                addData(temp_chart, time, temp);
                addData(humidity_chart, time, humidity);
            }

            if (cb)
                cb();
        }); */


});






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