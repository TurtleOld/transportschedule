import os
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_SERVER = os.getenv('DATABASE_SERVER')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')

if os.getenv('DATABASE_URL'):
    DATABASE_URL = os.getenv('DATABASE_URL')
    f'postgresql+asyncpg://{DATABASE_URL}'
else:
    DATABASE_URL = f'postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_SERVER}:{DATABASE_PORT}/{DATABASE_NAME}'


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
