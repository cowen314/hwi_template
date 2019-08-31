from source.messaging import PubSubMessageCenter
from source.engines import LoggerEngine, DaqEngine
from source.daq_drivers import SimulatedDaqDriver
from source.data_logging_drivers import TdmsLoggerDriver, FileLoggingSession, JsonLoggerDriver
from pathlib import Path
from nptdms import TdmsWriter, ChannelObject

if __name__ == "__main__":
    # logging to TDMS
    # logger = TdmsLoggerDriver()
    p = Path(".")

    logger = JsonLoggerDriver()
    logger.start_session(FileLoggingSession(Path("./test.json")))
    logger.write_data({"test_channel": [1,2,44,5]})
    logger.stop_session()

    # straight TDMS logging
    # with TdmsWriter(Path("./test1.tdms")) as tdms_writer:
    #     co = ChannelObject("this_is_a_group", "this_is_channel", [1, 2, 3])
    #     tdms_writer.write_segment([co])

    # logging DAQ data
    # daq = DaqEngine("daq engine", [SimulatedDaqDriver("simulated daq driver")])
    # logger = LoggerEngine(TdmsLoggerDriver())
    # logger.start_session(FileLoggingSession("C:\\Users\\cowen\\Desktop\\test.tdms"))
    # daq.read_and_pub_all_inputs()
    # pass

    # messaging
    # def listener(test_arg):
    #     print("An event occurred, this is being printed from the callback. Data: %s" % test_arg)
    # PubSubMessageCenter.subscribe(listener, "test")
    # PubSubMessageCenter.send_message("test", test_arg=123)
    # pass
