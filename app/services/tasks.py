from app.schemas.filters import FilteringParams
from app.schemas.tasks import TaskSchemaAdd, TaskSchemaEdit
from app.utils.unitofwork import IUnitOfWork
from app.config.tracer_setup import trace_manager


class TasksService:
    def __init__(self):
        self.tracer = trace_manager.get_tracer(__name__)

    async def add_task(self, uow: IUnitOfWork, task: TaskSchemaAdd):
        with self.tracer.start_as_current_span("Service: Add Task") as span:
            tasks_dict = task.model_dump()
            async with uow:
                task_id = await uow.tasks.add_one(tasks_dict)
                await uow.commit()
                span.set_attribute("task_id", task_id)
                return task_id

    async def get_tasks(self, uow: IUnitOfWork, filtering: FilteringParams):
        with self.tracer.start_as_current_span("Service: Get Tasks") as span:
            async with uow:
                tasks = await uow.tasks.find_all(
                    sort_order=filtering.sort_order,
                    page_size=filtering.page_size,
                    page=filtering.page
                )
                span.set_attribute("tasks.count", len(tasks))
                return tasks

    async def edit_task(self, uow: IUnitOfWork, task_id: int, task: TaskSchemaEdit):
        with self.tracer.start_as_current_span("Service: Edit Tasks") as span:
            tasks_dict = task.model_dump()
            async with uow:
                await uow.tasks.edit_one(task_id, tasks_dict)
                await uow.commit()
                span.set_attribute("task_id", task_id)
