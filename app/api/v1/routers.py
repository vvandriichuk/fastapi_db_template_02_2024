from app.api.v1.tasks import router as router_tasks
from app.api.v1.users import router as router_users

all_routers = [
    router_tasks,
    router_users,
]
