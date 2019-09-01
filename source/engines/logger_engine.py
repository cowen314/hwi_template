from source.engines._engines_shared import DATA_TOPIC
from source.messaging import PubSubMessageCenter


class LoggerEngine:
    def __init__(self, driver):
        self._driver = driver

    def _write_data(self, source_string, data):
        self._driver.write_data(data)

    def start_session(self, session):
        self._driver.start_session(session)
        PubSubMessageCenter.subscribe(self._write_data, DATA_TOPIC)

    def stop_session(self):
        PubSubMessageCenter.unsubscribe(self._write_data, DATA_TOPIC)
        self._driver.stop_session()