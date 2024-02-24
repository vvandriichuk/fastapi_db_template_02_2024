import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

# (/app/db)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# /app
APP_DIR = os.path.dirname(CURRENT_DIR)

# Go to root
PROJECT_ROOT = os.path.dirname(APP_DIR)

# Put db to root
DATABASE_URL = f"sqlite+aiosqlite:///{os.path.join(CURRENT_DIR, 'sqlite.db')}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


Base = declarative_base()


async def get_async_session():
    async with async_session_maker() as session:
        yield session
