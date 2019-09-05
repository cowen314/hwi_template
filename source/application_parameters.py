from abc import abstractmethod
from pathlib import Path
from source.constants import APP_NAME, GROUP_NAME, CONFIG_FILE_DIRECTORY
import json
from threading import Lock


class _ApplicationParameters:
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
    _parameters_dict = None
    _lock = Lock()

    @staticmethod
    def open_connection():
        try:
            path = LocalFileParameters._build_parameters_file_path()
            backup_path = path / Path(".bak")
            backup_path.touch()
            with open(backup_path, "w+") as file_ref:
                json.dump(LocalFileParameters._parameters_dict, file_ref)  # create a backup copy of the file in case anything goes wrong
            with open(path, "r+") as file_ref:
                LocalFileParameters._parameters_dict = json.load(file_ref)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            LocalFileParameters._parameters_dict = {}

    @staticmethod
    def read(section_name):
        return LocalFileParameters._parameters_dict[section_name]

    @staticmethod
    def write(section_name, data):
        with LocalFileParameters._lock:
            LocalFileParameters._parameters_dict.get[section_name] = data
            try:
                with open(LocalFileParameters._build_parameters_file_path(), mode="w+") as file_ref:  # FIXME? this might be a bit slow
                    json.dump(LocalFileParameters._parameters_dict, file_ref)
            except FileNotFoundError:
                path = LocalFileParameters._build_parameters_file_path()
                path.parent.mkdir(parents=True, exist_ok=True)  # create the file structure
                path.touch()  # generate
                with open(path, mode="w+") as file_ref:
                    json.dump(LocalFileParameters._parameters_dict, file_ref)

    @staticmethod
    def close_connection():
        LocalFileParameters._parameters_dict = None

    @staticmethod
    def _build_parameters_file_path():
        return CONFIG_FILE_DIRECTORY / Path(GROUP_NAME) / Path(APP_NAME) / Path("application_parameters.json")
