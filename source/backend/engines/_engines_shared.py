from abc import abstractmethod

DATA_TOPIC = "data"


class _EngineMessage:
    @abstractmethod
    def execute(self, engine_ref):
        raise NotImplementedError


def build_key(channel_name: str, driver_name: str = None, engine_name: str = None) -> str:
    key = ""
    if engine_name:
        key += (engine_name + ".")
    if driver_name:
        key += (driver_name + ".")
    key += channel_name
    return key
