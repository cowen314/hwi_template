from abc import abstractmethod
import random


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
    def read_data(self):
        """
        :return: dict { channel_name: values[] }
        """
        raise NotImplementedError

    @abstractmethod
    def write_data(self, data):
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

    def read_data(self):
        return {"simulated channel": [random.random()]}

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