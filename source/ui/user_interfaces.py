from abc import abstractmethod


class _UserInterface:
    @abstractmethod
    def update_display_by_state(self, state):
        pass


class CommandLineInterface(_UserInterface):
    def update_display_by_state(self, state):
        pass