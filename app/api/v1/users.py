from fastapi import APIRouter

from api.v1.dependencies import UOWDep, CurrentUser
from schemas.users import UserSchemaAdd
from services.users import UsersService

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
    user_id = await UsersService().add_user(uow, user)
    return {"user_id": user_id}


@router.get("")
async def get_users(
    uow: UOWDep,
    current_user: CurrentUser,
):
    users = await UsersService().get_users(uow)
    return users
