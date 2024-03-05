from fastapi import APIRouter

from opentelemetry import trace

from app.api.v1.dependencies import UOWDep, CurrentUser
from app.schemas.users import UserSchemaAdd
from app.services.users import UsersService

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
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("Add User Endpoint"):
        user_id = await UsersService().add_user(uow, user)
        return {"user_id": user_id}


@router.get("")
async def get_users(
    uow: UOWDep,
    current_user: CurrentUser,
):
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("Get User Endpoint"):
        users = await UsersService().get_users(uow)
        return users
