from typing import Optional

from opentelemetry import trace

from app.schemas.tasks import TaskSchemaAdd, TaskSchemaEdit
from app.utils.unitofwork import IUnitOfWork

tracer = trace.get_tracer(__name__)


class TasksService:
    async def add_task(self, uow: IUnitOfWork, task: TaskSchemaAdd):
        with tracer.start_as_current_span("Service: Add Task") as span:
            tasks_dict = task.model_dump()
            async with uow:
                task_id = await uow.tasks.add_one(tasks_dict)
                await uow.commit()
                span.set_attribute("task_id", task_id)
                return task_id

    async def get_tasks(self, uow: IUnitOfWork, sort_order: str = "ASC", page_size: int = 10, page: int = 1, author_id: Optional[int] = None, assignee_id: Optional[int] = None):
        with tracer.start_as_current_span("Service: Get Tasks") as span:
            async with uow:
                tasks = await uow.tasks.find_all(sort_order=sort_order, page_size=page_size, page=page, author_id=author_id, assignee_id=assignee_id)
                span.set_attribute("tasks.count", len(tasks))
                return tasks

    async def edit_task(self, uow: IUnitOfWork, task_id: int, task: TaskSchemaEdit):
        with tracer.start_as_current_span("Service: Edit Tasks") as span:
            tasks_dict = task.model_dump()
            async with uow:
                await uow.tasks.edit_one(task_id, tasks_dict)
                await uow.commit()
                span.set_attribute("task_id", task_id)
