from abc import abstractmethod
from pathlib import Path
from source.constants import APP_NAME, GROUP_NAME, CONFIG_FILE_DIRECTORY
import json
from threading import Lock
from source.backend.application_parameters.application_parameter_sections import ALL_PARAMETERS


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
    __parameters_dict = {}
    __lock = Lock()

    @staticmethod
    def initialize():
        # ensure that the appropriate file exists
        try:
            path = LocalFileParameters._build_parameters_file_path()
            with open(path, "r+") as file_ref:
                LocalFileParameters.__parameters_dict = json.load(file_ref)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            LocalFileParameters.__parameters_dict = {}

        # ensure that all sections are properly populated
        for param_section in ALL_PARAMETERS:
            try:
                LocalFileParameters.read(param_section)
            except KeyError:
                LocalFileParameters.__parameters_dict[param_section.__name__] = param_section()
        print(LocalFileParameters.__parameters_dict)
        with open(LocalFileParameters._build_parameters_file_path(), mode="w+") as file_ref:
            json.dump(LocalFileParameters._convert_params_dict_to_json(), file_ref)

        # backup_path = LocalFileParameters._build_parameters_file_path().with_suffix(".json.bak")
        # backup_path.touch()
        # with open(backup_path, "w+") as file_ref:
        #     json.dump(LocalFileParameters._convert_params_dict_to_json(),
        #               file_ref)  # create a backup copy of the file in case anything goes wrong

    @staticmethod
    def read(section_class):
        # try this as an object first
        if section_class not in ALL_PARAMETERS:
            raise TypeError("'section_class' must be in ALL_PARAMETERS")
        return LocalFileParameters.__parameters_dict[section_class.__name__]

    @staticmethod
    def write(data):
        """
        Write a section to file
        :param data: a section to write the the application parameters file
        """
        with LocalFileParameters.__lock:
            data_class = data.__class__
            if data_class not in ALL_PARAMETERS:
                raise TypeError("'data' must be in ALL_PARAMETERS")

            LocalFileParameters.__parameters_dict[data_class.__name__] = data
            try:
                with open(LocalFileParameters._build_parameters_file_path(), mode="w+") as file_ref:  # FIXME? this might be a bit slow
                    json.dump(LocalFileParameters._convert_params_dict_to_json(), file_ref)
            except FileNotFoundError:
                path = LocalFileParameters._build_parameters_file_path()
                path.parent.mkdir(parents=True, exist_ok=True)  # create the file structure
                path.touch()
                with open(path, mode="w+") as file_ref:
                    json.dump(LocalFileParameters._convert_params_dict_to_json(), file_ref)

    # @staticmethod
    # def _section_obj_to_json(obj):
    #     json.loads(obj)

    @staticmethod
    def _json_to_section_obj(section_class):
        jsn = LocalFileParameters.__parameters_dict[section_class.__name__]
        section_class(**jsn)

    @staticmethod
    def _convert_params_dict_to_json():
        # flatten the parameters objects
        a = {}
        for k, v in LocalFileParameters.__parameters_dict.items():
            a[k] = v.to_json()
        return a


    @staticmethod
    def deinitialize():
        LocalFileParameters.__parameters_dict = None

    @staticmethod
    def _build_parameters_file_path():
        return CONFIG_FILE_DIRECTORY / Path(GROUP_NAME) / Path(APP_NAME) / Path("application_parameters.json")
