from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.db import Base
from app.schemas.users import UserSchema


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    tasks = relationship("Tasks", back_populates="author")

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            name=self.name,
            tasks=[task.to_read_model() for task in self.tasks] if self.tasks else None,
        )
