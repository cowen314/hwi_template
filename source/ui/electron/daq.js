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
        if (this.readyState == 4){
            var data = JSON.parse(this.responseText);
            var rows = ""
            data["data"].forEach(value => {
                var row = "<tr>"
                row += "<td>" + toString(value.name) + "</td>" + "<td>" + toString(value.value) + "</td>" 
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
    var trace1 = {
        x: [1, 2, 3, 4],
        y: [10, 15, 13, 17],
        type: 'scatter',
      };
      
      var trace2 = {
        x: [1, 2, 3, 4],
        y: [16, 5, 11, 9],
        type: 'scatter'
      };
      
      var data = [trace1, trace2];
      
      Plotly.newPlot(plotElementId, data, {}, {showSendToCloud: true});
}

  
  