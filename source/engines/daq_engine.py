import time
from enum import Enum
from abc import abstractmethod
from transitions import Machine
import threading
from source.engines._engines_shared import _EngineMessage, DATA_TOPIC
from source.messaging import PubSubMessageCenter

DAQ_MESSAGE_TOPIC = "daq"


class StartDaqMessage(_EngineMessage):
    def execute(self, daq_engine):
        daq_engine.start_daq_requested()


class DaqEngineStates(Enum):
    IDLE = 0
    RUNNING = 1


class DaqEngine:
    def __init__(self, name, drivers):
        self.name = name
        self._periodic_read_thread = None
        self._periodic_read_thread_stop_event = threading.Event()
        self._drivers = drivers
        PubSubMessageCenter.subscribe(self._handle_daq_messsage, DAQ_MESSAGE_TOPIC)
        self.machine = Machine(model=self, states=[i.name for i in DaqEngineStates], initial=DaqEngineStates.IDLE)
        self.machine.add_transition(trigger="start_daq_requested",
                                    source=DaqEngineStates.IDLE,
                                    dest=DaqEngineStates.RUNNING,
                                    after=self._start_periodic_daq_reads)

    def read_and_pub_all_inputs(self):
        for driver in self._drivers:
            PubSubMessageCenter.send_message(DATA_TOPIC, source_string=driver.name, data=driver.read_data())
        # return [("a", driver.read_data()) for driver in self._drivers]

    def _handle_daq_messsage(self, message):
        message.execute(self)
        # if message == "start_daq":
        #     pass

    def _start_periodic_daq_reads(self):
        for driver in self._drivers:
            driver.start()
        self._periodic_read_thread = threading.Thread(target=self._periodic_read_process,
                                            args=(self._periodic_read_thread_stop_event))
        self._periodic_read_thread.run()
        """
        FIXME if this fails to execute for any reason, the state machine needs to be kicked back into a Idle state.
        it might make more sense to make this "action" occur on an internal event, then fire another event on a 
        success of this "action" to put the SM into the Running state
        """

    def _periodic_read_process(self, stop_event):
        while not stop_event.is_set():
            self.read_and_pub_all_inputs()
            time.sleep(1)

