from typing import List, Optional

from pydantic import BaseModel

from schemas.tasks import TaskSchema


class UserSchema(BaseModel):
    id: int
    name: str
    tasks: Optional[List[TaskSchema]] = None

    class Config:
        from_attributes = True


class UserSchemaAdd(BaseModel):
    name: str
