from source.application_parameters.application_parameters import LocalFileParameters
from enum import Enum


# class SectionNames(Enum):
#     User = 0


class _ParameterSection:
    pass


# TODO figure out how parameter sections will work... typing will probably have to be built into the
class UserParameters(_ParameterSection):
    def __init__(self, users):
        self.users = users


def write_section_by_class_name(obj):
    LocalFileParameters.write(type(obj).__name__, obj)


if __name__ == "__main__":
    user_input = input("Parameters sections may be overwritten. Enter 'Y' to proceed. Enter anything else to exit. Command: ")
    if user_input == 'Y':
        print("Writing parameter sections")
        LocalFileParameters.initialize()
        user_params = UserParameters(["co", "co", "to", "mo", "cd"])
        write_section_by_class_name(user_params)
        LocalFileParameters.deinitialize()
    else:
        print("Parameter sections will not be written")
    print("Exiting")
