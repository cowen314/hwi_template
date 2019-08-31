from abc import abstractmethod
from nptdms import TdmsWriter, ChannelObject
import numpy
import json

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


class JsonLoggerDriver(_LoggerDriver):
    def __init__(self):
        self._json_object = None
        self._file_path = None

    def start_session(self, session):
        self._file_path = session.file_path
        try:
            with open(self._file_path, mode="r+") as fh:
                self._json_object = json.load(fh)
        except FileNotFoundError or json.decoder.JSONDecodeError:
            self._json_object = {}

    def stop_session(self):
        with open(self._file_path, mode="w+") as fh:
            json.dump(self._json_object, fh)
        self._json_object = None
        self._file_path = None

    def write_data(self, data):
        for channel_name, data_values in data.items():
            channel_section = self._json_object.get(channel_name)
            if not channel_section:
                self._json_object[channel_name] = data_values
            else:
                channel_section[channel_name] += data_values  # append the new data values
