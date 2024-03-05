from fastapi import APIRouter

from opentelemetry import trace

from app.api.v1.dependencies import UOWDep, CurrentUser
from app.schemas.tasks import TaskSchemaAdd, TaskSchemaEdit
from app.services.tasks import TasksService

router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"],
)


@router.get("")
async def get_tasks(
    uow: UOWDep,
    current_user: CurrentUser,
):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("Get Tasks Endpoint"):
        tasks = await TasksService().get_tasks(uow)
        return tasks


@router.post("")
async def add_task(
    task: TaskSchemaAdd,
    uow: UOWDep,
    current_user: CurrentUser,
):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("Add Tasks Endpoint"):
        task_id = await TasksService().add_task(uow, task)
        return {"task_id": task_id}


@router.patch("/{id}")
async def edit_task(
    id: int,
    task: TaskSchemaEdit,
    uow: UOWDep,
    current_user: CurrentUser,
):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("Edit Tasks Endpoint"):
        await TasksService().edit_task(uow, id, task)
        return {"ok": True}
