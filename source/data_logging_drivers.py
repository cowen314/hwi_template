from abc import abstractmethod


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
    def write_data(self, data):
        pass  # TODO

    def start_session(self, session):
        pass  # TODO
