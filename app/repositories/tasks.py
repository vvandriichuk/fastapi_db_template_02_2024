from typing import Type

from db.db import Base
from models.tasks import Tasks
from utils.repository import SQLAlchemyRepository


class TasksRepository(SQLAlchemyRepository):
    @property
    def model(self) -> Type[Base]:
        return Tasks
