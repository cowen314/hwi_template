from abc import abstractmethod
from enum import Enum
from pathlib import Path
from transitions import Machine

from source.data_logging_drivers import FileLoggingSession
from source.engines.daq_engine import DAQ_MESSAGE_TOPIC, StartDaqMessage, StopDaqMessage
from source.engines.logger_engine import LOGGER_MESSAGE_TOPIC, LoggerStartMessage, LoggerStopMessage
from source.messaging import PubSubMessageCenter


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
        self.machine = Machine(model=self, states=[i.name for i in UserWorflowStates], initial=UserWorflowStates.LOGGED_OUT.name)
        self.machine.add_transition(
            trigger='login_succeeded',  # TODO figure out if events can be enumerated, that'd be nice
            source=UserWorflowStates.LOGGED_OUT.name,
            dest=UserWorflowStates.IDLE_MANUAL.name,
            # after=logged_in_callback
        )
        self.machine.add_transition(
            trigger='logout_succeeded',
            source=[UserWorflowStates.IDLE_MANUAL.name, UserWorflowStates.AUTO_TESTING.name],
            dest=UserWorflowStates.LOGGED_OUT.name,
            # after=disconnected_callback
        )
        self.machine.add_transition(
            trigger='start_testing_requested',
            source=UserWorflowStates.IDLE_MANUAL.name,
            dest=UserWorflowStates.AUTO_TESTING.name
        )
        self.machine.add_transition(
            trigger='stop_testing_requested',
            source=UserWorflowStates.AUTO_TESTING.name,
            dest=UserWorflowStates.IDLE_MANUAL.name
        )

    def run(self):
        """ hard implemented as command line for now, but can make this object-oriented later.
        Also, see description below for better handling"""
        while True:
            if self.state == UserWorflowStates.LOGGED_OUT.name:
                print("Logged out, enter credentials")  # on enter actions here
                while True:
                    user_input = input("Enter username: ")  # read from console input
                    if user_input == "co":  # TODO replace with parameters file lookup
                        self.login_succeeded()
                        break
                    else:
                        print("User not recognized")
            elif self.state == UserWorflowStates.IDLE_MANUAL.name:
                print("Manual control state entered."
                      "\nEnter 'sdaq' to start DAQ operations"
                      "\nEnter 'stest' to start logging data for a test"
                      "\nEnter 'logout' to logout")
                while True:
                    user_input = input("Command: ")
                    if user_input == "sdaq":
                        PubSubMessageCenter.send_message(DAQ_MESSAGE_TOPIC, message=StartDaqMessage())
                        print("Starting DAQ")
                    elif user_input == "stest":
                        # TODO need some way to start the logging operations
                        print("Starting testing/logging")
                        self.start_testing_requested()
                        break
                    elif user_input == "logout":
                        self.logout_succeeded()
                        break
            elif self.state == UserWorflowStates.AUTO_TESTING.name:
                print("Logging has started. A test may now be run.")
                PubSubMessageCenter.send_message(DAQ_MESSAGE_TOPIC, message=StartDaqMessage())
                PubSubMessageCenter.send_message(
                    LOGGER_MESSAGE_TOPIC,
                    message=LoggerStartMessage(FileLoggingSession(Path("./test.json"))))
                while True:
                    user_input = input("Enter 'stop' to return to manual control state: ")
                    if user_input == 'stop':
                        PubSubMessageCenter.send_message(LOGGER_MESSAGE_TOPIC, message=LoggerStopMessage())
                        PubSubMessageCenter.send_message(DAQ_MESSAGE_TOPIC, message=StopDaqMessage())
                        self.stop_testing_requested()
                        break



        # update the display
        # listen for and handle events. Events may change the state, cause the UI to update, etc.
        """
        how do events get fired? In the case of a command line interface, there'd need to be a loop sitting and
        waiting for input. if the loop received th correct credentials, it'd fire an event that'd end the current loop
        and start some new loop based on the next state. there wouldn't have to be an actual loop if there was a way to
        tie a callback to the enter key or something. We could just configure that callback when entering the LOGGED_OUT
        state, then disable it (if necessary) when logging in.
        """

