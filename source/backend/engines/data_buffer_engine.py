from source.messaging import _MessageCenter, PubSubMessageCenter
from abc import abstractmethod
from queue import Queue
from typing import List, Dict, Any, Tuple, Iterable, Generic, TypeVar

T = TypeVar('T')


class _BufferEngine(object):
    @abstractmethod
    def read_latest_value(self, key: str):
        raise NotImplementedError

    @abstractmethod
    # consider adding the ability to run this asynchronously, because we might want all of the subscription management
    # to happen asynchronously
    def write(self, key: str, value):
        """
        Write a single value to a key. If writing multiple values, use `write_multiple`
        :param key: the key to write to
        :param value: the value to write
        """
        raise NotImplementedError

    def write_multiple(self, key: str, values: Iterable):
        """
        Write multiple values to a key
        :param key: the key to write to
        :param values: the values to write
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_keys(self) -> Iterable[str]:
        """
        :return: all keys
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_keys_and_values(self, filter_by_type=None) -> Iterable[Tuple[str, Any]]:
        """
        :param filter_by_type: a type of value to filter by. If no value is set, all keys and values will be returned.
        :return: the keys and PRESENT values in the engine filtered by `filter_by_type`
        """
        raise NotImplementedError

    @abstractmethod
    def create_subscription(self, key: str) -> Queue:
        """
        Create a subscription to `key`, which provides lossless access to data published to `key`
        :param key: the key to create a subscription to
        :return: a Queue object. All values written to `key` will be pushed to this queue.
        """
        raise NotImplementedError

    @abstractmethod
    def close_subscription(self, queue: Queue):
        """
        Close a particular subscription.
        :param queue:
        """
        raise NotImplementedError

    @abstractmethod
    def close_all_subscriptions(self):
        """
        Close all active subscriptions.
        """
        raise NotImplementedError


class BufferEngine(_BufferEngine):
    def __init__(self):
        self._subscriptions: Dict[str, List[Queue]] = {}
        self._values: Dict[str, Any] = {}

    def read_latest_value(self, key: str):
        return self._values[key]

    def get_all_keys(self) -> Iterable[str]:
        return self._values.keys()

    def get_all_keys_and_values(self, filter_by_type=None) -> Iterable[Tuple[str, Any]]:
        # TODO figure out if the type output type can be of the type specified by `filter_by_type` (instead of `Any`)
        # not the best implementation here, but just want to get things working
        pairs = []
        if not filter_by_type:
            for k, v in self._values.items():
                pairs.append((k, v))
            return pairs

        # filter by value type
        for k, v in self._values.items():
            if type(v) is filter_by_type:
                pairs.append((k, v))
        return pairs
        # below is how I want to do this, but type checking doesn't like the first part, and the second returns an iter
        # if not filter_by_type:
        #     return list(self._values.items())
        # return filter(lambda x: type(x[1]) is filter_by_type, list(self._values.items()))

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
                "One or more of the subscription queues was full prior to this write. Some data has been lost."
            )

    def write_multiple(self, key: str, values: Iterable):
        queue_overrun_flag = False
        for value in values:
            try:
                self.write(key, value)
            except OverflowError:  # catch this so that all of the writes complete before an exception is thrown
                queue_overrun_flag = True
        if queue_overrun_flag:
            raise OverflowError(
                "One or more of the subscription queues was full prior to this write. Some data has been lost."
            )

    def create_subscription(self, key: str, max_queued_elements: int = 100) -> Queue:
        if key not in self._subscriptions:
            self._subscriptions[key] = []
        subscription_queue = Queue(max_queued_elements)
        self._subscriptions[key].append(subscription_queue)
        return subscription_queue

    def close_subscription(self, queue: Queue):
        found = False
        for sub_list in self._subscriptions.values():
            for sub_queue in sub_list:
                if sub_queue is queue:
                    found = True
                    sub_list.remove(sub_queue)
        if not found:
            raise ValueError("Could not find the specified queue in the subscription list")

    def close_all_subscriptions(self):
        for sub_list in self._subscriptions.values():
            for sub in sub_list:
                sub.empty()
        self._subscriptions = {}
