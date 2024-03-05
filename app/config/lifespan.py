from contextlib import asynccontextmanager


@asynccontextmanager
async def app_lifespan(app):
    ...

    yield

    ...
