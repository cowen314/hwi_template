import time
from enum import Enum
from random import random
from source.messaging import PubSubMessageCenter
from threading import Thread, Event

from transitions import Machine
from abc import ABCMeta, abstractmethod


"""This file is an example of how an engine could be used"""
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


class EngineTemplate:

    def __init__(self, name, driver, connected_callback, disconnected_callback):
        # TODO add type annotations to constructor parameters
        self.name = name
        self.machine = Machine(model=self, states=[i.name for i in TemplateEngineStates], initial=TemplateEngineStates.DISCONNECTED.name)
        self.machine.add_transition(
            trigger='_connect_succeeded',
            source=TemplateEngineStates.DISCONNECTED.name,
            dest=TemplateEngineStates.CONNECTED.name,
            conditions=self._attempt_connection,
            after=connected_callback
        )
        self.machine.add_transition(
            trigger='_disconnect_succeeded',
            before=self._disconnect,
            source=TemplateEngineStates.CONNECTED.name,
            dest=TemplateEngineStates.DISCONNECTED.name,
            after=disconnected_callback
        )

    """BEGIN TRANSITION HELPER METHODS"""
    # define transition helper methods here for all public transitions. These helpers:
    # - help enable auto complete
    # - provide an explicit declaration of "public" transitions
    # - decoration of transitions
    # - should NOT contain anything that depends on state

    def connect_requested(self):
        self._connect_succeeded()

    def disconnect_requested(self):
        self._disconnect_succeeded()

    """END TRANSITION HELPER METHODS"""

    def _attempt_connection(self):
        """
        :return: True if connection attempt succeeds, False otherwise
        """
        print("Attempting to connect")
        time.sleep(1)
        if random() > 0.5:
            print("Connect succeeded")
            return True
        else:
            print("Connect failed")
            return False

    def _disconnect(self):
        print("Attempting to disconnect")
        time.sleep(1)
        print("Disconnect succeeded")


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

    d = EngineTemplate("test", generic_connect_callback, generic_disconnect_callback)
    print("OK")
