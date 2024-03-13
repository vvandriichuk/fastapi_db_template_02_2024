from enum import Enum


class AbstractCustomStrEnum(str, Enum):
    def __new__(cls, value) -> str:
        obj = str.__new__(cls, value)
        obj._value_ = value
        return obj

    def __call__(self, *args, **kwargs) -> str:
        return self.value.format(*args, **kwargs)
