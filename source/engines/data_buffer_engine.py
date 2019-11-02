from ..messaging import _MessageCenter, PubSubMessageCenter
from abc import abstractmethod


class _InputHandler:
    @abstractmethod
    def process_input(self):
        pass

# TODO define concrete implementations of the above class


class DefaultInputHandler(_InputHandler):
    def __init__(self):
        pass

    def process_input(self):
        pass


class DataBufferEngine:
    def __init__(self, message_center: _MessageCenter = PubSubMessageCenter()):
        self._message_center = message_center
        self._input_handlers = []

    def add_input(self, topic: str, frames_to_buffer: int):
        # self._message_center.subscribe(self.process_input, )
        pass
