from abc import abstractmethod
from pathlib import Path


class _SystemParameters:
    # TODO add static prop

    @staticmethod
    @abstractmethod
    def read():
        pass

    @staticmethod
    @abstractmethod
    def write(section_name, data):
        pass


class Write