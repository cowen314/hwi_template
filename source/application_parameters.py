from abc import abstractmethod
from pathlib import Path
from source.constants import APP_NAME, GROUP_NAME
import json
from threading import Lock


class _ApplicationParameters:
    # TODO add static prop

    @staticmethod
    @abstractmethod
    def open_connection():
        pass

    @staticmethod
    @abstractmethod
    def read(section_name):
        pass

    @staticmethod
    @abstractmethod
    def write(section_name, data):
        pass

    @staticmethod
    @abstractmethod
    def close_connection():
        pass


class LocalFileParameters(_ApplicationParameters):
    _parameters_dict = None  # FIXME? is this the best way to create a static member
    _lock = Lock()  # TODO
    # file_ref = None
    @staticmethod
    def open_connection():
        global _parameters_dict
        try:
            with open(LocalFileParameters._build_parameters_file_path(), "r+") as file_ref:
                _parameters_dict = json.load(file_ref)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            _parameters_dict = {}

    @staticmethod
    def read(section_name):
        global _parameters_dict
        return _parameters_dict[section_name]

    @staticmethod
    def write(section_name, data):
        global _parameters_dict, _lock
        with _lock:
            _parameters_dict[section_name] = data
            with open(LocalFileParameters._build_parameters_file_path(), mode="w+") as file_ref:  # FIXME? this might be a bit slow
                json.dump(_parameters_dict, file_ref)

    @staticmethod
    def close_connection():
        global file_ref, _parameters_dict
        file_ref.close()
        file_ref = None
        _parameters_dict = None

    @staticmethod
    def _build_parameters_file_path():
        # TODO get ProgramData (or equivalent) path constant
        return Path(".") / Path(GROUP_NAME) / Path(APP_NAME+".json")

