from abc import abstractmethod
from nptdms import TdmsWriter, ChannelObject
import numpy

class _LoggingSession:
    pass


class FileLoggingSession(_LoggingSession):
    def __init__(self, file_path):
        self.file_path = file_path


class _LoggerDriver:
    @abstractmethod
    def write_data(self, data):
        pass

    @abstractmethod
    def start_session(self, session):
        pass

    @abstractmethod
    def stop_session(self):
        pass


class TdmsLoggerDriver(_LoggerDriver):
    def __init__(self):
        self._tdms_writer = None

    def write_data(self, data):
        """
        write data to a TDMS file
        :param data: a dictionary of channel_name : data_values
        """
        # for channel_name, data_values in data.items():
        channels = [ChannelObject('group1', channel_name, data_values) for channel_name, data_values in data.items()]
        self._tdms_writer.write_segment(channels)

    def start_session(self, session):
        self._tdms_writer = TdmsWriter(session.file_path)
        self._tdms_writer.open()

    def stop_session(self):
        self._tdms_writer.close()
        self._tdms_writer = None