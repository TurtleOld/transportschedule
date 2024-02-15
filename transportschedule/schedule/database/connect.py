import os
from pathlib import Path
from icecream import ic
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


current_directory = Path(__file__).resolve().parent.parent.parent.parent
file_name = 'transportschedule.db'
file_path = os.path.abspath(os.path.join(current_directory, file_name))
ic(file_path)

engine = create_engine(f'sqlite+pysqlite:///{file_path}', echo=True)


class Base(DeclarativeBase):
    __abstract__ = True
