$(document).ready(function() {
    //Temp and humidity values received during this session
    var tempList = [];
    var humidityList = [];
    var timeList = [];


    //Create empty charts
    var temp_chart = make_chart(id = "temp_chart", title = "Temperature C");
    var humidity_chart = make_chart(id = "humidity_chart", title = "Humidity %");
    var chart_type = "realtime";

    //clientId = "markos"
    //Create a client instance
    const host = 'ws://broker.emqx.io:8083/mqtt';
    clientId = "asdasdasddasdda";
    const options = {
        keepalive: 60,
        clientId: clientId,
        protocolId: 'MQTT',
        protocolVersion: 4,
        clean: true,
        reconnectPeriod: 1000,
        connectTimeout: 30 * 1000,
    }

    console.log('Connecting mqtt client');
    const client = mqtt.connect(host, options);

    client.on('connect', () => {
        console.log('Client connected')

        client.subscribe('sensors');
    });

    client.on('error', (err) => {
        console.log('Connection error: ', err);
        client.end();
    });

    client.on('reconnect', () => {
        console.log('Reconnecting...');
    });

    client.on('message', (topic, message, packet) => {
        console.log('Received Message: ' + message.toString() + '\nOn topic: ' + topic)
    });

    for (i = 0; i < 100; i++) {
        client.publish('sensors', 'ws connection demo...!', { qos: 0, retain: false });
    }


    // called when a message arrives
    function onMessageArrived(message) {
        console.log("onMessageArrived:" + message.payloadString);
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
    }



});









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