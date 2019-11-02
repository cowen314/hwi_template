import unittest

from source.application_parameters.application_parameters import LocalFileParameters
from source.messaging import PubSubMessageCenter
from source.engines.daq_engine import DaqEngine
from source.drivers.daq_drivers import SimulatedDaqDriver
from transitions.core import MachineError
from source.engines.template_engine import EngineTemplate


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


# class TestEngineTemplate(unittest.TestCase):
#     @staticmethod
#     def connect_callback():
#         print("connect callback called")
#
#     @staticmethod
#     def disconnect_callback_called():
#         print("disconnect callback called")
#
#     templte_engine = EngineTemplate("Engine Template", None, connect_callback, disconnect_callback_called)
#
#     templte_engine.connect_requested()


class TestApplicationParameters(unittest.TestCase):
    def test_section_write_and_read(self):
        test_section_name = "test"
        test_data = [1, 2, 3, 4]
        LocalFileParameters.initialize()
        LocalFileParameters.write(test_section_name, test_data)
        self.assertEqual(LocalFileParameters.read(test_section_name), test_data)
        LocalFileParameters.deinitialize()


class TestDaqEngine(unittest.TestCase):
    def test_invalid_state_transitions(self):
        """
        engines should toss exception if transition are requested in the wrong state
        """
        daq_engine = DaqEngine("test_engine", [SimulatedDaqDriver("simulated_daq_driver")])
        self.assertRaises(MachineError, daq_engine.stop_daq_requested)
        daq_engine.start_daq_requested()
        self.assertRaises(MachineError, daq_engine.start_daq_requested)

    def test_add_publication_target(self):
        """
        the DAQ engine allow adding additional publication targets
        """
        daq_engine = DaqEngine("test_engine", [SimulatedDaqDriver("simulated_daq_driver")])
        daq_engine.add_publication_topic()
        # TODO finish this

    def test_data_writes(self):
        # TODO
        pass
