from fastapi import APIRouter

from app.api.v1.dependencies import UOWDep, CurrentUser, FilteringDep
from app.schemas.users import UserSchemaAdd
from app.services.users import UsersService
from app.config.tracer_setup import trace_manager

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)


@router.post("")
async def add_user(
    user: UserSchemaAdd,
    uow: UOWDep,
    current_user: CurrentUser,
):
    tracer = trace_manager.get_tracer(__name__)
    with tracer.start_as_current_span("Add User Endpoint"):
        user_id = await UsersService().add_user(uow, user)
        return {"user_id": user_id}


@router.get("")
async def get_users(
    uow: UOWDep,
    current_user: CurrentUser,
    filtering: FilteringDep,
):
    tracer = trace_manager.get_tracer(__name__)
    with tracer.start_as_current_span("Get User Endpoint"):
        users = await UsersService().get_users(
            uow,
            filtering
        )

        return users
