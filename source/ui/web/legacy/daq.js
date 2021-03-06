// Requests
function get_daq_state(daqStateElementId){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4){
            if (this.status == 200) {
                document.getElementById(daqStateElementId).innerHTML = this.responseText
            }
            else {
                document.getElementById(daqStateElementId).innerHTML = "Request error"
            }
        }
    }
    request.open("GET", "http://127.0.0.1:5001/daq/state", true);
    request.send();
}

function start_daq(daqStateElementId) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4){
            get_daq_state(daqStateElementId);
        }
    }
    request.open("GET", "http://127.0.0.1:5001/daq/start", true);
    request.send();
}

function stop_daq(daqStateElementId) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4){
            get_daq_state(daqStateElementId);
        }
    }
    request.open("GET", "http://127.0.0.1:5001/daq/stop", true);
    request.send();
}

function reset_daq_error(daqStateElementId) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4){
            get_daq_state(daqStateElementId);
        }
    }
    request.open("GET", "http://127.0.0.1:5001/daq/resetError", true);
    request.send();
}

function update_table(tableElementId) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200){
            var data = JSON.parse(this.responseText);
            var rows = ""
            data["data"].forEach(value => {
                var row = "<tr>"
                row += "<td>" + value.name + "</td>" + "<td>" + value.value + "</td>" 
                rows += row + "</tr>"
            });
            document.getElementById(tableElementId).innerHTML = rows
            // $('#' + tableElementId).html(rows);
        }
    }
    request.open("GET", "http://127.0.0.1:5001/daq/getCurrentKeysAndValues", true);
    request.send();
}

// DAQ Plot
// var Plotly = require("plotly.js-dist")
function generate_plot(plotElementId) {
    var Plotly = require("plotly.js-dist")
    // var trace1 = {
    //     x: [1, 2, 3, 4],
    //     y: [10, 15, 13, 17],
    //     type: 'scatter',
    //   };
    //   var trace2 = {
    //     x: [1, 2, 3, 4],
    //     y: [16, 5, 11, 9],
    //     type: 'scatter'
    //   };
    // var data = [trace1, trace2];
    //   Plotly.newPlot(plotElementId, data, {}, {showSendToCloud: true});

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200){
            var data = JSON.parse(this.responseText);
            var plotData = []
            for (i in data){
                data[i].forEach(value => {
                    plotData.concat({name: i, x: x, y: y})
                });
            }
            TESTER = document.getElementById(plotElementId);
            Plotly.newPlot( TESTER, [{
            x: [1, 2, 3, 4, 5],
            y: [1, 2, 4, 8, 16] }], { 
            margin: { t: 0 } }, {showSendToCloud:true} );
        }
    }
    request.open("GET", "http://127.0.0.1:5001/daq/getBufferedData", true);
    request.send();

}

function start_buffering(){
    var request = new XMLHttpRequest();
    var buffer_button_element = document.getElementById("buffer_button");
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200){
            buffer_button_element.innerHTML = (buffer_button_element.innerHTML == "Stop Plotting") ?  "Start Plotting" : "Stop Plotting";
        }
    }
    var url = (buffer_button_element.innerHTML == "Stop Plotting") ? "http://127.0.0.1:5001/daq/stopPlotBuffering" : "http://127.0.0.1:5001/daq/startPlotBuffering";
    request.open("GET", url, true);
    request.send();
}
  
  