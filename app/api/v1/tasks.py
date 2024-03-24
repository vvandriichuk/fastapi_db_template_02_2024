from fastapi import APIRouter, Query
from typing import Optional
import time

from app.api.v1.dependencies import UOWDep, CurrentUser
from app.schemas.tasks import TaskSchemaAdd, TaskSchemaEdit
from app.services.tasks import TasksService
from app.config.logger_setup import logger_manager
from app.config.tracer_setup import trace_manager
from app.config.metrics_setup import mm

router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"],
)

logger = logger_manager.get_logger()
tracer = trace_manager.get_tracer(__name__)


@router.get("")
async def get_tasks(
    uow: UOWDep,
    current_user: CurrentUser,
    sort_order: str = Query("ASC", description="Sort order: ASC or DESC"),
    page_size: int = Query(10, description="Number of tasks per page"),
    page: int = Query(1, description="Page number"),
    author_id: Optional[int] = Query(None, description="Filter by author's ID"),
    assignee_id: Optional[int] = Query(None, description="Filter by assignee's ID"),
):
    with tracer.start_as_current_span("Get Tasks Endpoint"):
        start_time = time.time()
        tasks = await TasksService().get_tasks(uow, sort_order=sort_order, page_size=page_size, page=page, author_id=author_id, assignee_id=assignee_id)

        mm.counter_add(22)
        mm.updown_counter_add(27)
        mm.histogram_record(29)

        elapsed_time = time.time() - start_time
        logger.info(f"Logger executed in {elapsed_time:.4f} seconds")
        logger.error("Run get_tasks logger")
        return tasks


@router.post("")
async def add_task(
    task: TaskSchemaAdd,
    uow: UOWDep,
    current_user: CurrentUser,
):
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
    with tracer.start_as_current_span("Edit Tasks Endpoint"):
        await TasksService().edit_task(uow, id, task)
        return {"ok": True}
