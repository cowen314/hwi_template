from flask import Flask, Response
from flask_socketio import SocketIO, join_room, emit, send
from .sample_engine import SampleEngine
from ....engines.daq_engine import DaqEngine
from ....engines.data_buffer_engine import BufferEngine
from ....drivers.daq_drivers import SimulatedDaqDriver, ReadData
from transitions.core import MachineError
import json
from ....messaging import PubSubMessageCenter
from typing import List, Tuple, Iterable
from queue import Queue

app = Flask(__name__)
socketio = SocketIO(app)
buffer_engine = BufferEngine()
daq_engine = DaqEngine("daq engine", [SimulatedDaqDriver("sim daq driver")], buffer_engine)
plot_subscriptions: List[Tuple[str, Queue]] = []


@app.route("/")
def main():
    return "test"


@socketio.on('test')
def test_from_client(data):
    print("Socket message received from server: %s" % data)


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


@app.route("/daq/getCurrentKeysAndValues")
def get_keys_and_values():
    be = buffer_engine.get_all_keys_and_values()  # TODO consider adding filtering by type here
    data = []
    for i in be:
        data.append({
            "name": i[0],
            "value": i[1][0]
        })
    return {
        "data": data
    }


@app.route("/daq/startPlotBuffering")
def start_buffering():
    buffer_engine.close_all_subscriptions()  # this is precautionary. Remove when other entities use the buffer engine.
    # TODO replace with many calls to buffer_engine.close_subscription()
    keys = buffer_engine.get_all_keys()
    for k in keys:
        queue = buffer_engine.create_subscription(k)
        plot_subscriptions.append((k, queue))
    return ""


@app.route("/daq/stopPlotBuffering")
def stop_buffering():
    # TODO replace with many calls to buffer_engine.close_subscription()
    buffer_engine.close_all_subscriptions()
    return ""


@app.route("/daq/getBufferedData")
def get_buffered_data():
    """
    return something with this syntax:
        ReturnType = Dict[keyName: str, PlotItem] where PlotItem = Dict[str(either `x` or `y`), List[float?]]
    """
    # "keyName": "key"
    # "values": [...]
    data = {}
    # for key, queue in plot_subscriptions:
    #     data[key] = map(lambda x: x., queue)
    for key, queue in plot_subscriptions:
        # data[key] = map(list, zip(*list(queue.queue)))  # convert list of tuples to separate lists
        # s = zip(*list(queue.queue))
        # data[key] = {
        #     "x": list(s[0]),
        #     "y": list(s[1])
        # }
        # FIXME the below implementation is poor, update it for better performance
        channel_data = {
            "x": [],
            "y": []
        }
        for item in list(queue.queue):
            channel_data["x"].append(item[0])
            channel_data["y"].append(item[1])
        queue.queue.clear()  # this might drop a sample here and there, but should be fine for display purposes
        data[key] = channel_data
    return data





if __name__ == "__main__":
    print("about to start the flask app...")
    socketio.run(host="127.0.0.1", port=5001)
