from opentelemetry import trace

from app.schemas.users import UserSchemaAdd
from app.utils.unitofwork import IUnitOfWork

tracer = trace.get_tracer(__name__)


class UsersService:
    async def add_user(self, uow: IUnitOfWork, user: UserSchemaAdd):
        with tracer.start_as_current_span("Service: Add User") as span:
            user_dict = user.model_dump()
            async with uow:
                user_id = await uow.users.add_one(user_dict)
                await uow.commit()
                span.set_attribute("user_id", user_id)
                return user_id

    async def get_users(self, uow: IUnitOfWork):
        with tracer.start_as_current_span("Service: Get Users") as span:
            async with uow:
                users = await uow.users.find_all()
                span.set_attribute("users.count", len(users))
                return users
