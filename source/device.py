from enum import Enum
from transitions import Machine


class Device:

    states = ['disconnected', 'connected']

    def __init__(self, name):
        self.name = name
        self.machine = Machine(model=self, states=Device.states, initial='disconnected')
        self.machine.add_transition(
            trigger='connect succeeded',
            source='disconnected',
            dest='connected'
        )
        self.machine.add_transition(
            trigger='disconnect succeeded',
            source='connected',
            dest='disconnected'
        )

    def connect(self):
        pass

    def disconnect(self):
        pass

    def write_outputs(self, values):
        pass

    def read_inputs(self):
        pass


class TemperatureChannels(Enum):
    LEFT_INPUT = 1,
    RIGHT_INPUT = 2


class HeaterChannels(Enum):
    HEATER_VOLTAGE = 1
