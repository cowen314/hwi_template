from enum import Enum

class Device:
    def __init__(self):
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
