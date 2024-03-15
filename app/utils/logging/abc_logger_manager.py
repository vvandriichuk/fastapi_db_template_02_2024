from abc import ABC, abstractmethod
import logging


class BaseLoggerManager(ABC):
    @abstractmethod
    def get_logger(self) -> logging.Logger:
        pass
