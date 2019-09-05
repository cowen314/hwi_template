from abc import abstractmethod
from enum import Enum
from transitions import Machine
from threading import Event, Thread


class SequencerStates(Enum):
    IDLE = 0
    RUNNING = 1


class SequencerStatus(Enum):
    Okay = 0
    InitializingSequence = 1
    Paused = 2
    Stopping = 3
    Aborting = 4
    Aborted = 5


"""
- No need to define an interface, for now. This is best suited as an engine, where the UI calls the event triggers
- it would ultimately be nice if we could marry the concept of an interface to the transitions triggers
- basically, some set of triggers would be defined, and as long as an engine implemented those triggers it would be
considered to have implemented the "interface".
- I suppose the tricky thing here is bidirectional flow of information -- these trigger interfaces make passing data to
the engines just fine, but they don't provide any standardized way of returning data to the caller.
- For the sequencer this is just fine, as the main "events" can all be considered void (they don't need to return data)
- after talking to Mark, I'm realizing that we'll definitely want to be able to pass back data from these methods to
callers
- in MVC terms, the engines make up the Model. They will be called by controllers. 
- **engines can define standard interfaces. controllers can call engine interface methods, and those engine methods can 
call transition triggers if a transition is needed.**
- there's still a reason to use the transitions library: it provides diagnostic logging, on-transition actions, and
nice state handling
- if we do this, we'll need to make sure that we appropriately ignore API calls based on state (e.g. ignore a request
to start daq if we're already in the 'DAQ Running' state)
"""
class Sequencer:
    def __init__(self):
        self.sequence = None
        self.machine = Machine(model=self, states=[i.name for i in SequencerStates], initial=SequencerStates.IDLE.name)
        self.machine.add_transition(
            trigger='idle_requested',
            source=SequencerStates.RUNNING.name,
            dest=SequencerStates.IDLE.name,
            before=self._stop_sequence
        )
        self.machine.add_transition(
            trigger='running_requested',
            source=SequencerStates.IDLE.name,
            dest=SequencerStates.RUNNING.name,
            before=self._kick_off_sequence
        )
        self.sequencer_status = SequencerStatus.Okay.name
        self._sequence_stop_event = Event()
        self._sequence_thread = Thread(target=self._sequence_task)

    def start(self, sequence):
        self.running_requested(sequence)

    def _kick_off_sequence(self, sequence):
        self.sequence = sequence
        self.stop_requested = False
        self._sequence_stop_event.clear()
        self._sequence_thread.start()

    def _sequence_task(self):
        # init sequence
        self.sequencer_status = SequencerStatus.InitializingSequence.name
        self.sequence.initialize()
        self.sequencer_status = SequencerStatus.Okay.name

        # execute sequence
        while self.sequence.has_next_step():
            self.sequence.execute_step(self._sequence_stop_event)  # TODO consider returning and handling step results here
            if self._sequence_stop_event.is_set():
                self.sequencer_status = SequencerStatus.Stopping
                break
            self.sequence.next_step()

        # cleanup sequence
        if self._sequence_stop_event:
            self.sequencer_status = SequencerStatus.Aborted.name
        else:
            self.sequencer_status = SequencerStatus.Okay.name

    # TODO consider implementing this in the future
    # def stop(self):
    #     pass

    # TODO implement later
    # @abstractmethod
    # def pause(self):
    #     pass
    #
    # @abstractmethod
    # def resume(self):
    #     pass

    def abort(self):
        self.idle_requested()

    def _stop_sequence(self):
        self.sequencer_status = SequencerStatus.Aborting.name
        self.sequence.abort()
        self._sequence_stop_event.set()


# FIXME at first glance, I dislike the idea of having a sequence status and a sequencer status. And we consolidate?
class Sequence_Status(Enum):
    Okay = 0
    Errored = 1
    Aborted = 2
    Pass = 3
    Failed = 4


class Sequence:
    pass
