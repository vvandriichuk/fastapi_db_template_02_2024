from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models.tasks import Tasks
from utils.repository import SQLAlchemyRepository


class TasksRepository(SQLAlchemyRepository):
    model = Tasks
