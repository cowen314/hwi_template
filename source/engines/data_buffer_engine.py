from ..messaging import _MessageCenter, PubSubMessageCenter
from abc import abstractmethod
from queue import Queue
from typing import List, Dict, Any, Tuple, Iterable


class _BufferEngine(object):
    @abstractmethod
    def read_latest_value(self, key: str):
        raise NotImplementedError

    @abstractmethod
    # consider adding the ability to run this asynchronously, because we might want all of the subscription management
    # to happen asynchronously
    def write(self, key: str, value):
        raise NotImplementedError

    @abstractmethod
    def get_all_keys(self) -> Iterable[str]:
        raise NotImplementedError

    @abstractmethod
    def get_all_keys_and_values(self) -> Iterable[Tuple[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def create_subscription(self, key: str) -> Queue:
        raise NotImplementedError


class BufferEngine(_BufferEngine):
    def __init__(self):
        self._subscriptions: Dict[str, List[Queue]] = {}
        self._values: Dict[str, Any] = {}

    def read_latest_value(self, key: str):
        return self._values[key]

    def get_all_keys(self) -> Iterable[str]:
        return self._values.keys()

    def get_all_keys_and_values(self) -> Iterable[Tuple[str, Any]]:
        # not the best implementation here, but just want to get things working
        pairs = []
        for k, v in self._values.items():
            pairs.append((k, v))
        return pairs

    def write(self, key: str, value):
        self._values[key] = value
        queue_overrun_flag = False
        if key in self._subscriptions:
            for subscription_queue in self._subscriptions[key]:
                if subscription_queue.full():
                    queue_overrun_flag = True
                    subscription_queue.get_nowait()
                subscription_queue.put_nowait(value)
        if queue_overrun_flag:
            raise OverflowError(
                "One or more of the subscription queues was full prior to this write. Some data has been lost.")

    def create_subscription(self, key: str, max_queued_elements: int = 100) -> Queue:
        if key not in self._subscriptions:
            self._subscriptions[key] = []
        subscription_queue = Queue(max_queued_elements)
        self._subscriptions[key].append(subscription_queue)
        return subscription_queue
