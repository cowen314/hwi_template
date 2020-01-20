import time
from enum import Enum
import traceback
from transitions import Machine
import threading
from ._engines_shared import _EngineMessage, DATA_TOPIC
from ..messaging import PubSubMessageCenter, _MessageCenter
from typing import List
from ..drivers.daq_drivers import _DaqDriver
from .data_buffer_engine import _BufferEngine
from ._engines_shared import build_key

DAQ_MESSAGE_TOPIC = "daq"

# FIXME? do we need a messaging infrastructure? Can we just do this all via events?
# the main argument for messaging, as I see it, is that it allows nice communication between state machines.
# there's probably a much better way to make that happen though...


class StartDaqMessage(_EngineMessage):
    def execute(self, engine_ref):
        engine_ref.start_daq_requested()


class StopDaqMessage(_EngineMessage):
    def execute(self, engine_ref):
        engine_ref.stop_daq_requested()


class DaqEngineStates(Enum):
    IDLE = 0
    RUNNING = 1
    ERROR = 2


class DaqEngine:
    def __init__(self, name: str, drivers: List[_DaqDriver], buffer_engine: _BufferEngine,
                 message_center: _MessageCenter = PubSubMessageCenter(), wait_time: float = 0.1):
        """
        :param name: a name to identify this engine
        :param drivers: an array of drivers to be used for data collection
        :param message_center: reference to a message center used for publishing data
        :param wait_time: the time, in seconds, to wait between R/W cycles
        """
        self.name = name
        self._periodic_read_thread = None
        self._periodic_read_thread_stop_event = threading.Event()
        self._drivers = drivers
        self._message_center = message_center
        self.wait_time = wait_time
        self._buffer_engine = buffer_engine

        # define connections
        self._message_center.subscribe(self._handle_daq_messsage, DAQ_MESSAGE_TOPIC)

        # define state logic
        self.machine = Machine(model=self, states=[i.name for i in DaqEngineStates], initial=DaqEngineStates.IDLE.name)
        self.machine.add_transition(
            trigger="_start_daq_requested",
            source=DaqEngineStates.IDLE.name,
            dest=DaqEngineStates.RUNNING.name,
            after=self._start_periodic_daq_reads)
        self.machine.add_transition(
            trigger="_stop_daq_requested",
            source=DaqEngineStates.RUNNING.name,
            dest=DaqEngineStates.IDLE.name,
            after=self._stop_periodic_daq_reads
        )
        self.machine.add_transition(
            trigger="_error_occurred",
            source=DaqEngineStates.IDLE.name,
            dest=DaqEngineStates.ERROR.name
        )
        self.machine.add_transition(
            trigger="_error_occurred",
            source=DaqEngineStates.RUNNING.name,
            dest=DaqEngineStates.ERROR.name,
            after=self._stop_periodic_daq_reads
        )
        self.machine.add_transition(
            trigger="_reset_error_requested",
            source=DaqEngineStates.ERROR.name,
            dest=DaqEngineStates.IDLE.name
        )

    """BEGIN TRANSITION HELPER METHODS"""
    # define transition helper methods here for all PUBLIC transitions. These helpers:
    # - help enable auto complete
    # - provide an explicit declaration of "public" transitions
    # - allow decoration of transitions
    # - should NOT contain anything that depends on state

    def start_daq_requested(self):
        self._start_daq_requested()

    def stop_daq_requested(self):
        self._stop_daq_requested()

    def reset_error_requested(self):
        self._reset_error_requested()

    """END TRANSITION HELPER METHODS"""

    def _read_and_pub_all_inputs(self):
        for driver in self._drivers:
            # there are a few options here:

            # (1) publish to the message center
            data = driver.read_data()
            # self._message_center.send_message(DATA_TOPIC, source_string=driver.name)
            # TODO make DATA_TOPIC a parameter, add support for adding / removing topics

            # (2) publish to the buffer engine
            for channel_name, values in data.items():
                self._buffer_engine.write(build_key(channel_name, driver_name=driver.name), values)

    def _handle_daq_messsage(self, message):
        message.execute(self)

    def _start_periodic_daq_reads(self):
        try:
            for driver in self._drivers:
                driver.start()
            self._periodic_read_thread = threading.Thread(
                target=self._periodic_read_process,
                kwargs={"stop_event": self._periodic_read_thread_stop_event})  # FIXME get this working with regular old args
            self._periodic_read_thread_stop_event.clear()
            self._periodic_read_thread.start()
        except Exception:
            traceback.print_exc()
            self._error_occurred()

    def _stop_periodic_daq_reads(self):
        self._periodic_read_thread_stop_event.set()

    def _periodic_read_process(self, stop_event=None):
        try:
            while not stop_event.is_set():
                self._read_and_pub_all_inputs()
                time.sleep(self.wait_time)
        except Exception:
            traceback.print_exc()
            self._error_occurred()
