from abc import abstractmethod

DATA_TOPIC = "data"


class _EngineMessage:
    @abstractmethod
    def execute(self, daq_engine):
        pass
