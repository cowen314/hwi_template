from enum import Enum

"""
Include all application specific parameters here.
Parameters can be broken into logical sections.
Use key word arguments in all section parameter __init__ methods
"""

# class SectionNames(Enum):
#     User = 0


class _ParameterSection:
    def to_json(self):
        """
        :return: something that's json serializable.
        """
        return self.__dict__


class UserParameters(_ParameterSection):
    def __init__(self, users=None):
        if users is None:
            users = [""]
        self.users = users


""" Place all parameter sections in ALL_PARAMETERS"""
ALL_PARAMETERS = [
    UserParameters
]
