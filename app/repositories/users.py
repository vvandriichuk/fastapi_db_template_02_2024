from typing import Any, Type
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import selectinload

from app.db.db import Base
from app.models.users import Users
from app.utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    @property
    def model(self) -> Type[Base]:
        return Users

    async def find_all(
            self,
            sort_order: str = "ASC",
            page_size: int = 10,
            page: int = 1,
            **filters: Any
    ):
        query = select(self.model).options(selectinload(self.model.tasks))

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
        return [user.to_read_model() for user in res.scalars().all()]
