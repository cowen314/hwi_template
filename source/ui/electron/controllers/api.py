from flask import Flask, Response
from .sample_engine import SampleEngine
from ....engines.daq_engine import DaqEngine
from ....engines.data_buffer_engine import BufferEngine
from ....drivers.daq_drivers import SimulatedDaqDriver
from transitions.core import MachineError
from ....messaging import PubSubMessageCenter

# class FlaskLauncher:
#     def __init__(self):

app = Flask(__name__)
buffer_engine = BufferEngine()
daq_engine = DaqEngine("daq engine", [SimulatedDaqDriver("sim daq driver")], buffer_engine)


@app.route("/")
def main():
    return "test"


@app.route("/data_example")
def data_example():
    engine = SampleEngine()
    data = engine.get_sample_data()
    return data.__dict__


@app.route("/daq/data")
def daq_data():
    pass


@app.route("/daq/start")
def start_daq():
    try:
        daq_engine.start_daq_requested()
        return ""
    except MachineError:
        return "Already in the requested state"


@app.route("/daq/resetError")
def reset_daq_error():
    try:
        daq_engine.reset_error_requested()
        return ""
    except MachineError:
        return "Either not in error state, or error reset failed"


@app.route("/daq/stop")
def stop_daq():
    try:
        daq_engine.stop_daq_requested()
        return ""
    except MachineError:
        return "Already in the requested state"


@app.route("/daq/state")
def daq_state():
    return daq_engine.state


if __name__ == "__main__":
    print("about to start the flask app...")
    app.run(host="127.0.0.1", port=5001)
