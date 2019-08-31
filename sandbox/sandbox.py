from source.messaging import PubSubMessageCenter
from source.engines import LoggerEngine, DaqEngine
from source.daq_drivers import SimulatedDaqDriver
from source.data_logging_drivers import TdmsLoggerDriver, FileLoggingSession

if __name__ == "__main__":
    daq = DaqEngine("daq engine", [SimulatedDaqDriver("simulated daq driver")])
    logger = LoggerEngine(TdmsLoggerDriver())
    logger.start_session(FileLoggingSession("C:\\Users\\cowen\\Desktop\\test.tdms"))
    daq.read_and_pub_all_inputs()
    pass

    # messaging
    # def listener(test_arg):
    #     print("An event occurred, this is being printed from the callback. Data: %s" % test_arg)
    # PubSubMessageCenter.subscribe(listener, "test")
    # PubSubMessageCenter.send_message("test", test_arg=123)
    # pass
