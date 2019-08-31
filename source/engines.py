import time
from enum import Enum
from random import random
from source.messaging import PubSubMessageCenter

from transitions import Machine
from abc import ABCMeta, abstractmethod

DATA_TOPIC = "data"


class TemplateEngineStates(Enum):
    CONNECTED = 0
    DISCONNECTED = 1
    ERROR = 2


class _EngineTemplate:
    # states = ['disconnected', 'connected']  # leaving this here to remind one that states can also just be strings

    def __init__(self, name, driver, connected_callback, disconnected_callback):
        self.name = name
        self.machine = Machine(model=self, states=[i.name for i in TemplateEngineStates], initial=TemplateEngineStates.DISCONNECTED)
        self.machine.add_transition(
            trigger='connect_succeeded',
            source='disconnected',
            dest=TemplateEngineStates.CONNECTED,
            after=connected_callback
        )
        self.machine.add_transition(
            trigger='disconnect_succeeded',
            source='connected',
            dest=TemplateEngineStates.DISCONNECTED,
            after=disconnected_callback
        )

    def connect(self):
        print("Attempting to connect")
        time.sleep(1)
        if random() > 0.5:
            print("Connect succeeded")
            self.connect_succeeded(self)
        else:
            print("Connect failed")

    def disconnect(self):
        print("Attempting to disconnect")
        time.sleep(1)
        print("Disconnect succeeded")
        self.disconnect_succeeded(self)


'''
ok so the class gets decorated with events ...
great...
but what if I want to call a method A and depending on the outcome, potentially change states
well, you could have a method C that wraps A with the state transition logic
could you do this differently?
yeah, probably.
you could create an internal transition that runs some method B.
Method B would essentially do what method C does.
Looks like the best way might just be the former.
'''


class DaqEngine:
    def __init__(self, name, drivers):
        self.name = name
        self._drivers = drivers

    def read_and_pub_all_inputs(self):
        for driver in self._drivers:
            PubSubMessageCenter.send_message(DATA_TOPIC, source_string=driver.name, data=driver.read_data())
        # return [("a", driver.read_data()) for driver in self._drivers]


class LoggerEngine:
    def __init__(self, driver):
        self._driver = driver

    def _write_data(self, source_string, data):
        self._driver.write_data(data)

    def start_session(self, session):
        self._driver.start_session(session)
        PubSubMessageCenter.subscribe(self._write_data, DATA_TOPIC)

    def stop_session(self):
        PubSubMessageCenter.unsubscribe(self._write_data, DATA_TOPIC)
        self._driver.stop_session()


if __name__ == "__main__":
    def generic_connect_callback(device):
        print("Callback: %s connected" % device.name)

    def generic_disconnect_callback(device):
        print("Callback: %s disconnected" % device.name)

    d = _EngineTemplate("test", generic_connect_callback, generic_disconnect_callback)
    print("OK")

'''
what's an effective way to pass parameters to callbacks?
'''