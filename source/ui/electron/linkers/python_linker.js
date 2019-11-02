function get_stuff_from_python_example() {
    // var python = require("python-shell")
    var path = require("path")

    pythonArg = document.getElementById("pythonArgument").value
    var options = {
        scriptPath : path.join(__dirname, '../engine/'),
        args : [pythonArg]
    }

    // var pythonOutput = new python('python_example.py', options)

    // pythonOutput.on('message', function(message) {
    //     swal(message);
    // })
}