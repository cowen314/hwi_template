from enum import Enum
from transitions import Machine
from source.engines._engines_shared import DATA_TOPIC, _EngineMessage
from source.messaging import PubSubMessageCenter


LOGGER_MESSAGE_TOPIC = "logger"


class LoggerEngineStates(Enum):
    IDLE = 0
    LOGGING = 1


class LoggerStartMessage(_EngineMessage):
    def execute(self, engine_ref):
        engine_ref.start_logging_requested()


class LoggerStopMessage(_EngineMessage):
    def execute(self, engine_ref):
        engine_ref.stop_logging_requested()

"""
The general structure of engine constructors:
- setup class members
- setup transitions / state logic
- setup messaging
"""
class LoggerEngine:
    def __init__(self, driver):
        self._driver = driver
        self.machine = Machine(model=self, states=[s.name for s in LoggerEngineStates], initial=LoggerEngineStates.IDLE)
        self.machine.add_transition(  # TODO make this an internal event, then add another event to be fired if the start_logging request is successful
            trigger='start_logging_requested',
            source=LoggerEngineStates.IDLE,
            dest=LoggerEngineStates.LOGGING,
            after=self._start_session  # TODO figure out how to pass session parameters from the caller to the callback
        )
        self.machine.add_transition(  # TODO make this an internal event, then add another event to be fired if the start_logging request is successful
            trigger='stop_logging_requested',
            source=LoggerEngineStates.LOGGING,
            dest=LoggerEngineStates.IDLE,
            after=self._stop_session  # TODO figure out how to pass session parameters from the caller to the callback
        )
        PubSubMessageCenter.subscribe(self._handle_message, LOGGER_MESSAGE_TOPIC)

    def _handle_message(self, message):
        message.execute(self)

    def _write_data(self, source_string, data):
        self._driver.write_data(data)

    def _start_session(self, session):
        self._driver.start_session(session)
        PubSubMessageCenter.subscribe(self._write_data, DATA_TOPIC)

    def _stop_session(self):
        PubSubMessageCenter.unsubscribe(self._write_data, DATA_TOPIC)
        self._driver.stop_session()
