$(document).ready(function() {
    //Temp and humidity values received during this session
    var tempList = [];
    var humidityList = [];
    var timeList = [];

    //Create empty charts
    var temp_chart = make_chart(id = "temp_chart", title = "Temperature C");
    var humidity_chart = make_chart(id = "humidity_chart", title = "Humidity %");
    var chart_type = "realtime";




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
    });





});









//Adds data point to chart
function addData(chart, label, data) {
    //label = get_hours_mins(label);
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}

function get_hours_mins(time) {
    var date = new Date(parseInt(time));
    return date.toLocaleTimeString(navigator.language, {
        hour: '2-digit',
        minute: '2-digit'
    });
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
            labels: [],
            data: [],
            datasets: [{
                data: [],
                label: "Africa",
                borderColor: "#3e95cd",
                fill: false
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
                        unit: 'second',
                        format: "HH:MM:SS"
                    },
                    ticks: {
                        maxTicksLimit: 5
                    }
                }
            }

        }
    });
    return chart;
}