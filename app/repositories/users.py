from typing import Type
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.db import Base
from app.models.users import Users
from app.utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    @property
    def model(self) -> Type[Base]:
        return Users

    async def find_all(self):
        stmt = select(self.model).options(selectinload(self.model.tasks))
        res = await self.session.execute(stmt)
        users = [row[0].to_read_model() for row in res.all()]
        return users
