from threading import Thread, Event
from time import sleep

class Subsystem:
    def __init__(self):
        pass

    def _process(self, *args, **kwargs):
        pass

    def start_daemon(self):
        pass


class TemperatureController(Subsystem):
    def __init__(self, temp_input_device, heater_output_device):
        self._temp_dev = temp_input_device
        self._heater_dev = heater_output_device
        self.setpoint = None
        self._daemon = Thread()
        self._stop_event = Event()

    def _process(self):
        while not self._stop_event.is_set():
            self._temp_dev.read()
            sleep(1)

    def start_daemon(self):
        self._stop_event.clear()
        self._daemon = Thread(target=self._process)
        self.daemon.run()
