from abc import abstractmethod
import random
from typing import Dict, List
from datetime import datetime


class ReadData:
    def __init__(self, timestamp: datetime, value: float):
        self.timestamp = timestamp
        self.value = value


class _DaqDriver:
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    @abstractmethod
    def read_data(self) -> Dict[str, List[ReadData]]:
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

    def read_data(self) -> Dict[str, List[ReadData]]:
        return {"simulated channel": [ReadData(datetime.now(), random.random())]}

    def write_data(self, data):
        pass


class NiDaqDriver(_DaqDriver):
    def __init__(self, name, task):
        super().__init__(name)
        self._task = task

    def read_data(self):
        return self._task.read()

    def write_data(self, data):
        self._task.write(data)  # might have to add some special formatting for the data