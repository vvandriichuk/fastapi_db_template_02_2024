from abc import ABC, abstractmethod
from typing import Type
from opentelemetry import trace

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update

from app.db.db import Base


class AbstractRepository(ABC):
    @property
    @abstractmethod
    def model(self) -> Type[Base]:
        pass

    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, id: int, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, **filter_by):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    @property
    def model(self) -> Type[Base]:
        raise NotImplementedError("Model must be defined by SQLAlchemyRepository subclasses")

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("UsersRepository: add_one"):
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await self.session.execute(stmt)
            return res.scalar_one()

    async def edit_one(self, id: int, data: dict) -> int:
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("UsersRepository: edit_one"):
            stmt = (
                update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
            )
            res = await self.session.execute(stmt)
            return res.scalar_one()

    async def find_all(self):
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("UsersRepository: find_all"):
            stmt = select(self.model)
            res = await self.session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res

    async def find_one(self, **filter_by):
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("UsersRepository: find_one"):
            stmt = select(self.model).filter_by(**filter_by)
            res = await self.session.execute(stmt)
            res = res.scalar_one().to_read_model()
            return res
