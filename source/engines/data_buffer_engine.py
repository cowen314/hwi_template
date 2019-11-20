from ..messaging import _MessageCenter, PubSubMessageCenter
from abc import abstractmethod
from queue import SimpleQueue
from typing import List, Dict, Any


class _BufferEngine(object):
    @abstractmethod
    def read_latest_value(self, key: str):
        raise NotImplementedError

    @abstractmethod
    def write(self, key: str, value, synchronous: bool = False):
        raise NotImplementedError

    @abstractmethod
    def create_subscription(self, key: str) -> SimpleQueue:
        raise NotImplementedError


class BufferEngine(_BufferEngine):
    def __init__(self):
        self._subscriptions: Dict[str, List[SimpleQueue]] = {}
        self._values: Dict[str, Any] = {}

    def read_latest_value(self, key: str):
        return self._values[key]

    def write(self, key: str, value, synchronous: bool = False):
        self._values[key] = value
        if key in self._subscriptions:
            for subscription_queue in self._subscriptions[key]:
                subscription_queue.put(value, block=False)

    def create_subscription(self, key: str) -> SimpleQueue:
        if key not in self._subscriptions:
            self._subscriptions[key] = []
        subscription_queue = SimpleQueue()
        self._subscriptions[key].append(subscription_queue)
        return subscription_queue
