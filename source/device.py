import time
from enum import Enum
from random import random

from transitions import Machine
from abc import ABCMeta, abstractmethod


class DeviceStates(Enum):
    CONNECTED = 0
    DISCONNECTED = 1
    ERROR = 2


class _Device:  # TODO implement ABCMeta
    # states = ['disconnected', 'connected']  # leaving this here to remind one that states can also just be strings

    def __init__(self, name, connected_callback, disconnected_callback):
        self.name = name
        self.machine = Machine(model=self, states=[i.name for i in DeviceStates], initial=DeviceStates.DISCONNECTED)
        self.machine.add_transition(
            trigger='connect_succeeded',
            source='disconnected',
            dest=DeviceStates.CONNECTED,
            after=connected_callback
        )
        self.machine.add_transition(
            trigger='disconnect_succeeded',
            source='connected',
            dest=DeviceStates.DISCONNECTED,
            after=disconnected_callback
        )

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass


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


class SimulatedDevice(_Device):
    def __init__(self, name, connect_callback, disconnect_callback):
        super().__init__(name, connect_callback, disconnect_callback)
        # able to add states here... not sure if you'd want to though

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

    # def write_value(self):
    #     if self.state is


class TemperatureChannels(Enum):
    LEFT_INPUT = 1,
    RIGHT_INPUT = 2


class HeaterChannels(Enum):
    HEATER_VOLTAGE = 1


if __name__ == "__main__":
    def generic_connect_callback(device):
        print("Callback: %s connected" % device.name)

    def generic_disconnect_callback(device):
        print("Callback: %s disconnected" % device.name)

    d = SimulatedDevice("test", generic_connect_callback, generic_disconnect_callback)
    print("OK")