from abc import abstractmethod
from enum import Enum
import time
from datetime import datetime, timedelta


# TODO either use this or get rid of it
class StepStatus(Enum):
    Okay = 0
    Errored = 1
    Aborted = 2
    Pass = 3
    Failed = 4


class _Step:
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def execute_step(self, stop_event):
        pass

    @abstractmethod
    def deinitialize(self):
        pass


class WaitStep(_Step):
    def __init__(self, _wait_time_seconds):
        self._wait_time_seconds = _wait_time_seconds

    def initialize(self):
        pass

    def execute_step(self, stop_event):
        start_time = datetime.now()
        while not stop_event.is_set():
            time.sleep(0.01)
            if (datetime.now() - start_time) > timedelta(seconds=self._wait_time_seconds):
                break

    def deinitialize(self):
        pass
