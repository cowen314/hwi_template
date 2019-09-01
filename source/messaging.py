from abc import abstractmethod
from pubsub import pub

"""
These are implementations of a pub-sub based messaging infrastructure
"""


class _MessageCenter:
    @staticmethod
    @abstractmethod
    def subscribe(listener_callback, topic):
        pass

    @staticmethod
    @abstractmethod
    def send_message(topic, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def unsubscribe(listener_callback, topic):
        pass


class PubSubMessageCenter(_MessageCenter):
    """
    This class uses the pubsub library
    https://pypubsub.readthedocs.io/en/v4.0.3/index.html
    """

    @staticmethod
    def subscribe(listener_callback, topic):
        pub.subscribe(listener_callback, topic)

    @staticmethod
    def send_message(topic, **kwargs):
        pub.sendMessage(topic, **kwargs)

    @staticmethod
    def unsubscribe(listener_callback, topic):
        pub.unsubscribe(listener_callback, topic)
