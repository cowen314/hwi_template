from enum import Enum


# class SectionNames(Enum):
#     User = 0


class _ParameterSection:
    pass


# TODO figure out how parameter sections will work... typing will probably have to be built into the
class UserParameters(_ParameterSection):
    def __init__(self, users):
        self.users = users