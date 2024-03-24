from abc import ABC, abstractmethod
from typing import Any, Dict, List, Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, desc, asc

from app.db.db import Base
from app.config.tracer_setup import trace_manager


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
    async def find_all(self, sort_order: str = "ASC", page_size: int = 10, page: int = 1, **filters: Any) -> List[Dict]:
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
        tracer = trace_manager.get_tracer(__name__)
        with tracer.start_as_current_span("UsersRepository: add_one"):
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await self.session.execute(stmt)
            return res.scalar_one()

    async def edit_one(self, id: int, data: dict) -> int:
        tracer = trace_manager.get_tracer(__name__)
        with tracer.start_as_current_span("UsersRepository: edit_one"):
            stmt = (
                update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
            )
            res = await self.session.execute(stmt)
            return res.scalar_one()

    async def find_all(self, sort_order: str = "ASC", page_size: int = 10, page: int = 1, **filters: Any) -> List[Dict]:
        tracer = trace_manager.get_tracer(__name__)
        with tracer.start_as_current_span("UsersRepository: find_all"):
            query = select(self.model)

            for key, value in filters.items():
                if value is not None and hasattr(self.model, key):
                    column = getattr(self.model, key)
                    query = query.filter(column == value)

            if sort_order.upper() == "DESC":
                query = query.order_by(desc(self.model.id))
            else:
                query = query.order_by(asc(self.model.id))

            query = query.offset((page - 1) * page_size).limit(page_size)

            res = await self.session.execute(query)
            return [row.to_read_model() for row in res.scalars().all()]

    async def find_one(self, **filter_by):
        tracer = trace_manager.get_tracer(__name__)
        with tracer.start_as_current_span("UsersRepository: find_one"):
            stmt = select(self.model).filter_by(**filter_by)
            res = await self.session.execute(stmt)
            res = res.scalar_one().to_read_model()
            return res
