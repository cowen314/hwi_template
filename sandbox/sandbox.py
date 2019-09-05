from source.engines.daq_engine import DaqEngine
from source.engines.logger_engine import LoggerEngine
from source.engines.user_workflow_engine import UserWorkflowEngine
from source.messaging import PubSubMessageCenter
from source.daq_drivers import SimulatedDaqDriver
from source.data_logging_drivers import TdmsLoggerDriver, FileLoggingSession, JsonLoggerDriver
from pathlib import Path
from nptdms import TdmsWriter, ChannelObject


if __name__ == "__main__":
    # logging to JSON or TDMS
    # logger = TdmsLoggerDriver()
    # p = Path(".")
    # logger = JsonLoggerDriver()
    # logger.start_session(FileLoggingSession(Path("./test.json")))
    # logger.start_session(FileLoggingSession(Path("./test.tdms")))
    # logger.write_data({"test_channel": [1,2,44,5]})
    # logger.stop_session()

    # straight TDMS logging
    # with TdmsWriter(Path("./test1.tdms")) as tdms_writer:
    #     co = ChannelObject("this_is_a_group", "this_is_channel", [1, 2, 3])
    #     tdms_writer.write_segment([co])

    # logging DAQ data
    # daq = DaqEngine("daq engine", [SimulatedDaqDriver("simulated daq driver")])
    # logger = LoggerEngine(TdmsLoggerDriver())
    # logger = LoggerEngine(JsonLoggerDriver())
    # logger.start_session(FileLoggingSession(Path("./test.json")))
    # daq.read_and_pub_all_inputs()
    # pass
    # logger.stop_session()

    # User workflows
    daq_engine = DaqEngine("daq engine", [SimulatedDaqDriver("simulated driver")])
    logger_engine = LoggerEngine(JsonLoggerDriver())
    wf_engine = UserWorkflowEngine()
    wf_engine.run()

    # messaging
    # def listener(test_arg):
    #     print("An event occurred, this is being printed from the callback. Data: %s" % test_arg)
    # PubSubMessageCenter.subscribe(listener, "test")
    # PubSubMessageCenter.send_message("test", test_arg=123)
    # pass

    # try:
    #     raise FileNotFoundError
    # except (FileExistsError, FileNotFoundError):
    #     print("Successfully caught error")

    # variable scope testing
    # def outer():
    #     x = "local"
    #
    #     def inner():
    #         nonlocal x
    #         print("inner pre assign: ", x)
    #         x = "nonlocal"
    #         print("inner post assign:", x)
    #
    #     inner()
    #     print("outer:", x)
    # outer()
