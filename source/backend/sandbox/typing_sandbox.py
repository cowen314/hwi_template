from typing import Type, List, Tuple, Generic, Union


class Parent1:
    def method1(self):
        pass


class Parent2:
    def method2(self):
        pass


class Child(Parent1, Parent2):
    pass


# For now, maybe `Union` can be used to imply multiple inheritance
def some_function(param: Union[Parent1, Parent2]):
    param.method1()
    param.method2()
