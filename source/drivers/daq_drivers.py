from abc import abstractmethod
import random
from typing import Dict, Iterable, Tuple
from datetime import datetime

# wrapping this data into a class made serialization more difficult. The type alias seems to work nicely.
ReadData = Tuple[datetime, float]


class _DaqDriver(object):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    @abstractmethod
    def read_data(self) -> Dict[str, Iterable[ReadData]]:
        raise NotImplementedError

    @abstractmethod
    def write_data(self, data: Dict[str, float]):
        """
        :param data: dict { channel_name: values[] }
        """
        raise NotImplementedError


class SimulatedDaqDriver(_DaqDriver):
    def __init__(self, name):
        super().__init__(name)

    def start(self):
        pass

    def stop(self):
        pass

    def read_data(self) -> Dict[str, Iterable[ReadData]]:
        return {
            "simulated channel": [(datetime.now(), random.random())],
            "simulated channel 2": [(datetime.now(), random.random())]
        }

    def write_data(self, data):
        pass


class NiDaqDriver(_DaqDriver):
    def __init__(self, name, task):
        super().__init__(name)
        self._task = task

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def read_data(self):
        return self._task.read()

    def write_data(self, data):
        self._task.write(data)  # might have to add some special formatting for the data