from abc import abstractmethod, ABC
from pathlib import Path
from source.constants import APP_NAME, GROUP_NAME, CONFIG_FILE_DIRECTORY
import json
from threading import Lock
from source.application_parameters.application_parameter_sections import _ParameterSection


class _ApplicationParameters:
    @staticmethod
    @abstractmethod
    def initialize():
        pass

    @staticmethod
    @abstractmethod
    def read(section_class):
        """
        :param section_class: a _ParameterSection child class specifier
        """
        pass

    @staticmethod
    @abstractmethod
    def write(data):
        """
        :param data: a child of _ParameterSection
        """
        pass

    @staticmethod
    @abstractmethod
    def deinitialize():
        pass


class LocalFileParameters(_ApplicationParameters):
    __parameters_dict = None
    __lock = Lock()

    @staticmethod
    def initialize():
        try:
            path = LocalFileParameters._build_parameters_file_path()
            backup_path = path / Path(".bak")
            backup_path.touch()
            with open(backup_path, "w+") as file_ref:
                json.dump(LocalFileParameters.__parameters_dict, file_ref)  # create a backup copy of the file in case anything goes wrong
            with open(path, "r+") as file_ref:
                LocalFileParameters.__parameters_dict = json.load(file_ref)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            LocalFileParameters.__parameters_dict = {}

    @staticmethod
    def read(section_class):
        # try this as an object first
        if not issubclass(section_class, _ParameterSection):
            raise TypeError("'section_class' must be a child of _ParameterSection")
        return LocalFileParameters.__parameters_dict[section_class.__name__]

    @staticmethod
    def write(data):
        with LocalFileParameters.__lock:
            data_class = data.__class__
            if not issubclass(data_class, _ParameterSection):
                raise TypeError("'data' must be a child of _ParameterSection")

            LocalFileParameters.__parameters_dict.get[data_class.__name__] = data
            try:
                with open(LocalFileParameters._build_parameters_file_path(), mode="w+") as file_ref:  # FIXME? this might be a bit slow
                    json.dump(LocalFileParameters.__parameters_dict, file_ref)
            except FileNotFoundError:
                path = LocalFileParameters._build_parameters_file_path()
                path.parent.mkdir(parents=True, exist_ok=True)  # create the file structure
                path.touch()
                with open(path, mode="w+") as file_ref:
                    json.dump(LocalFileParameters.__parameters_dict, file_ref)

    @staticmethod
    def _section_obj_to_json(obj):
        # TODO
        pass

    @staticmethod
    def _json_to_section_obj(jsn, section_class):
        # TODO
        pass

    @staticmethod
    def deinitialize():
        LocalFileParameters.__parameters_dict = None

    @staticmethod
    def _build_parameters_file_path():
        return CONFIG_FILE_DIRECTORY / Path(GROUP_NAME) / Path(APP_NAME) / Path("application_parameters.json")
