import unittest
from source.messaging import PubSubMessageCenter
from time import sleep


class TestMessagingClasses(unittest.TestCase):
    def test_pub_sub(self):
        callback_called = False
        arg_received = None
        arg_passed = 1234

        def listener(test_arg):
            global callback_called
            callback_called = True
            global arg_received
            arg_received = test_arg
        PubSubMessageCenter.subscribe(listener, "test")
        PubSubMessageCenter.send_message("test", test_arg=arg_passed)
        # sleep(1)
        self.assertTrue(callback_called)
        self.assertEqual(arg_passed, arg_received)


class TestEngineTemplate(unittest.TestCase):
    # TODO
    pass
