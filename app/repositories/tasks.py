from typing import Type

from app.db.db import Base
from app.models.tasks import Tasks
from app.utils.repository import SQLAlchemyRepository


class TasksRepository(SQLAlchemyRepository):
    @property
    def model(self) -> Type[Base]:
        return Tasks
