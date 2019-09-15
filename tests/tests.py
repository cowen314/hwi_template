import unittest

from source.application_parameters.application_parameters import LocalFileParameters
from source.messaging import PubSubMessageCenter


class TestMessagingClasses(unittest.TestCase):
    def test_pub_sub(self):
        callback_called = False
        arg_received = None
        arg_passed = 1234

        def listener(test_arg):
            nonlocal callback_called, arg_received
            callback_called = True
            arg_received = test_arg
        PubSubMessageCenter.subscribe(listener, "test")
        PubSubMessageCenter.send_message("test", test_arg=arg_passed)
        # sleep(1)
        self.assertTrue(callback_called)
        self.assertEqual(arg_passed, arg_received)


class TestEngineTemplate(unittest.TestCase):
    # TODO
    pass


class TestApplicationParameters(unittest.TestCase):
    def test_section_write_and_read(self):
        test_section_name = "test"
        test_data = [1, 2, 3, 4]
        LocalFileParameters.initialize()
        LocalFileParameters.write(test_section_name, test_data)
        self.assertEqual(LocalFileParameters.read(test_section_name), test_data)
        LocalFileParameters.deinitialize()
