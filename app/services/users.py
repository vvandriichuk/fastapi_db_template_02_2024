from app.schemas.filters import FilteringParams
from app.schemas.users import UserSchemaAdd
from app.utils.unitofwork import IUnitOfWork
from app.config.tracer_setup import trace_manager


class UsersService:
    def __init__(self):
        self.tracer = trace_manager.get_tracer(__name__)

    async def add_user(self, uow: IUnitOfWork, user: UserSchemaAdd):
        with self.tracer.start_as_current_span("Service: Add User") as span:
            user_dict = user.model_dump()
            async with uow:
                user_id = await uow.users.add_one(user_dict)
                await uow.commit()
                span.set_attribute("user_id", user_id)
                return user_id

    async def get_users(self, uow: IUnitOfWork, filtering: FilteringParams):
        with self.tracer.start_as_current_span("Service: Get Users") as span:
            async with uow:
                users = await uow.users.find_all(
                    sort_order=filtering.sort_order,
                    page_size=filtering.page_size,
                    page=filtering.page
                )
                span.set_attribute("users.count", len(users))
                return users
