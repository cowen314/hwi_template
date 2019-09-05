import time
from enum import Enum
from random import random
from source.messaging import PubSubMessageCenter
from threading import Thread, Event

from transitions import Machine
from abc import ABCMeta, abstractmethod


"""This file is mostly just an example of how an engine might be used"""
# TODO add a messaging example


class TemplateEngineStates(Enum):
    CONNECTED = 0
    DISCONNECTED = 1
    ERROR = 2


# TODO consider doing something like this. transition triggers would be set to <enum_item>.name.
# this could be a bit weird I guess... need to think on it more
class TemplateEngineEvents(Enum):
    connect_requested = 0
    disconnect_requested = 1


class _EngineTemplate:
    # states = ['disconnected', 'connected']  # leaving this here to remind one that states can also just be strings

    def __init__(self, name, driver, connected_callback, disconnected_callback):
        self.name = name
        self.machine = Machine(model=self, states=[i.name for i in TemplateEngineStates], initial=TemplateEngineStates.DISCONNECTED.name)
        self.machine.add_transition(
            trigger='connect_succeeded',
            source=TemplateEngineStates.DISCONNECTED.name,
            dest=TemplateEngineStates.CONNECTED.name,
            after=connected_callback
        )
        self.machine.add_transition(
            trigger='disconnect_succeeded',
            source=TemplateEngineStates.CONNECTED.name,
            dest=TemplateEngineStates.DISCONNECTED.name,
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


if __name__ == "__main__":
    def generic_connect_callback(device):
        print("Callback: %s connected" % device.name)

    def generic_disconnect_callback(device):
        print("Callback: %s disconnected" % device.name)

    d = _EngineTemplate("test", generic_connect_callback, generic_disconnect_callback)
    print("OK")
