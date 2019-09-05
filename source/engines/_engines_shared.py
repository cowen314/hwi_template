from abc import abstractmethod

DATA_TOPIC = "data"


class _EngineMessage:
    @abstractmethod
    def execute(self, engine_ref):
        pass
