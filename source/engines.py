import time
from enum import Enum
from random import random
from source.messaging import PubSubMessageCenter
from threading import Thread, Event

from transitions import Machine
from abc import ABCMeta, abstractmethod

DATA_TOPIC = "data"
DAQ_MESSAGE_TOPIC = "daq"


class TemplateEngineStates(Enum):
    CONNECTED = 0
    DISCONNECTED = 1
    ERROR = 2


class _EngineTemplate:
    # states = ['disconnected', 'connected']  # leaving this here to remind one that states can also just be strings

    def __init__(self, name, driver, connected_callback, disconnected_callback):
        self.name = name
        self.machine = Machine(model=self, states=[i.name for i in TemplateEngineStates], initial=TemplateEngineStates.DISCONNECTED)
        self.machine.add_transition(
            trigger='connect_succeeded',
            source='disconnected',
            dest=TemplateEngineStates.CONNECTED,
            after=connected_callback
        )
        self.machine.add_transition(
            trigger='disconnect_succeeded',
            source='connected',
            dest=TemplateEngineStates.DISCONNECTED,
            after=disconnected_callback
        )

    def connect(self):
        print("Attempting to connect")
        time.sleep(1)
        if random() > 0.5:
            print("Connect succeeded")
            self.connect_succeeded(self)
        else:
            print("Connect failed")

    def disconnect(self):
        print("Attempting to disconnect")
        time.sleep(1)
        print("Disconnect succeeded")
        self.disconnect_succeeded(self)


'''
ok so the class gets decorated with events ...
great...
but what if I want to call a method A and depending on the outcome, potentially change states
well, you could have a method C that wraps A with the state transition logic
could you do this differently?
yeah, probably.
you could create an internal transition that runs some method B.
Method B would essentially do what method C does.
Looks like the best way might just be the former.
'''


class _DaqMessage:
    @abstractmethod
    def execute(self, daq_engine):
        pass


class StartDaqMessage(_DaqMessage):
    def execute(self, daq_engine):
        daq_engine.start_daq_requested()


class DaqEngineStates(Enum):
    IDLE = 0
    RUNNING = 1


class DaqEngine:
    def __init__(self, name, drivers):
        self.name = name
        self._periodic_read_thread = None
        self._periodic_read_thread_stop_event = Event()
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
        self._periodic_read_thread = Thread(target=self._periodic_read_process,
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


class UserWorflowStates(Enum):
    LOGGED_OUT = 0,  # Logged out, waiting for credentials
    IDLE_MANUAL = 1,  # Logged in, but no test is running. User has manual control.
    AUTO_TESTING = 2  # Logged in, a test is running. User does not have manual control


class _WorkflowState:
    @abstractmethod
    def display_text(self):
        pass


class UserWorkflowEngine:
    def __init__(self):
        # TODO figure out how to enable logging
        self.machine = Machine(model=self, states=[i.name for i in UserWorflowStates], initial=UserWorflowStates.LOGGED_OUT)
        self.machine.add_transition(
            trigger='login_succeeded',  # TODO figure out if events can be enumerated, that'd be nice
            source=UserWorflowStates.LOGGED_OUT,
            dest=UserWorflowStates.IDLE_MANUAL,
            # after=logged_in_callback
        )
        self.machine.add_transition(
            trigger='logout_succeeded',
            source=[UserWorflowStates.IDLE_MANUAL, UserWorflowStates.AUTO_TESTING],
            dest=UserWorflowStates.LOGGED_OUT,
            # after=disconnected_callback
        )
        self.machine.add_transition(
            trigger='testing_started',
            source=UserWorflowStates.IDLE_MANUAL,
            dest=UserWorflowStates.AUTO_TESTING
        )

    def run(self):
        """ hard implemented as command line for now, but can make this object-oriented later.
        Also, see description below for better handling"""
        while True:
            if self.state == UserWorflowStates.LOGGED_OUT:
                print("Logged out, enter credentials")  # on enter actions here
                while True:
                    user_input = "co"  # read from console input
                    if user_input == "co":
                        self.login_succeeded()
                        break
            elif self.state == UserWorflowStates.IDLE_MANUAL:
                print("Manual control state entered."
                      "Enter 'sdaq' to start DAQ operations"
                      "Enter 'stest' to start logging data for a test"
                      "Enter 'logout' to logout")
                while True:
                    user_input = ""
                    if user_input == "sdaq":
                        PubSubMessageCenter.send_message(DAQ_MESSAGE_TOPIC, message=StartDaqMessage())
                        print("Starting DAQ")
                    elif user_input == "slog":
                        # TODO need some way to start the logging operations
                        print("Starting testing/logging")
                        self.testing_started()
                    elif user_input == "logout":
                        self.logout_succeeded()
                        break
            elif self.state == UserWorflowStates.AUTO_TESTING:
                print("Logging has started. A test may now be run.")
                # TODO finish this

        # update the display
        # listen for and handle events. Events may change the state, cause the UI to update, etc.
        """
        how do events get fired? In the case of a command line interface, there'd need to be a loop sitting and
        waiting for input. if the loop received th correct credentials, it'd fire an event that'd end the current loop
        and start some new loop based on the next state. there wouldn't have to be an actual loop if there was a way to
        tie a callback to the enter key or something. We could just configure that callback when entering the LOGGED_OUT
        state, then disable it (if necessary) when logging in.
        """



if __name__ == "__main__":
    def generic_connect_callback(device):
        print("Callback: %s connected" % device.name)

    def generic_disconnect_callback(device):
        print("Callback: %s disconnected" % device.name)

    d = _EngineTemplate("test", generic_connect_callback, generic_disconnect_callback)
    print("OK")
