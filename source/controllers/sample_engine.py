from typing import Type
from random import random


class DataPackage(object):
    def __init__(self):
        self.samples = [()]

    def add_sample(self, timestamp, value):
        self.samples.append((timestamp, value))


class SampleEngine(object):
    def __init__(self):
        self._data = None

    def get_sample_data(self) -> DataPackage:
        d = DataPackage()
        for i in range(100):
            d.add_sample(i, random())
        return d
