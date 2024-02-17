import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_SERVER = os.getenv('DATABASE_SERVER')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')


DATABASE_URL = f'postgresql+asyncpg:///{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_SERVER}:{DATABASE_PORT}/{DATABASE_NAME}'

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)
async_session = AsyncSession(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
