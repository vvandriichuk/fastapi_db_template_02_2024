from enum import Enum


class AbstractCustomStrEnum(str, Enum):
    def __call__(self, *args, **kwargs) -> str:
        return self.value.format(*args, **kwargs)
