from sqlalchemy.orm import relationship
from app.models.tasks import Tasks
from app.models.users import Users

Users.tasks = relationship(
    "Tasks", back_populates="author", foreign_keys=[Tasks.author_id]
)
Tasks.author = relationship(
    "Users", back_populates="tasks", foreign_keys=[Tasks.author_id]
)
Tasks.assignee = relationship("Users", foreign_keys=[Tasks.assignee_id])
