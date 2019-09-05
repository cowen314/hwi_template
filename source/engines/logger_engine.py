from enum import Enum
from transitions import Machine
from ._engines_shared import DATA_TOPIC, _EngineMessage
from ..messaging import PubSubMessageCenter


LOGGER_MESSAGE_TOPIC = "logger"


class LoggerEngineStates(Enum):
    IDLE = 0
    LOGGING = 1


class LoggerStartMessage(_EngineMessage):
    def __init__(self, session):
        self.session = session

    def execute(self, engine_ref):
        engine_ref.start_logging_requested(self.session)


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
        self.machine = Machine(model=self, states=[s.name for s in LoggerEngineStates], initial=LoggerEngineStates.IDLE.name)
        self.machine.add_transition(

            # TODO make this an internal event, then add another event to be fired if the start_logging request is
            # successful... or maybe leave it the way it is, and add some sort of default fault behavior that dumps the
            # engine into an error state. ORRRR use the optional conditions parameter to pass in callbacks that must
            # return True if the transition is to take place

            trigger='start_logging_requested',
            source=LoggerEngineStates.IDLE.name,
            dest=LoggerEngineStates.LOGGING.name,
            after=self._start_session  # TODO figure out how to pass session parameters from the caller to the callback
        )
        self.machine.add_transition(  # TODO make this an internal event, then add another event to be fired if the stop_logging request is successful
            trigger='stop_logging_requested',
            source=LoggerEngineStates.LOGGING.name,
            dest=LoggerEngineStates.IDLE.name,
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
