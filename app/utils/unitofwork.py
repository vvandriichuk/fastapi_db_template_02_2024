from abc import ABC, abstractmethod
from opentelemetry import trace

from app.db.db import async_session_maker
from app.repositories.tasks import TasksRepository
from app.repositories.users import UsersRepository


class IUnitOfWork(ABC):
    users: UsersRepository
    tasks: TasksRepository

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker
        self.tracer = trace.get_tracer(__name__)

    async def __aenter__(self):
        with self.tracer.start_as_current_span("UnitOfWork: Start"):
            self.session = self.session_factory()

            self.users = UsersRepository(self.session)
            self.tasks = TasksRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        with self.tracer.start_as_current_span("UnitOfWork: Exit"):
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
            await self.session.close()

    async def commit(self):
        with self.tracer.start_as_current_span("UnitOfWork: Commit"):
            await self.session.commit()

    async def rollback(self):
        with self.tracer.start_as_current_span("UnitOfWork: Rollback"):
            await self.session.rollback()