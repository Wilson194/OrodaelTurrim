from enum import Enum


class AutoNumber(Enum):
    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class LogicalOperator(AutoNumber):
    AND = ()
    OR = ()


    def __str__(self):
        return self.name
