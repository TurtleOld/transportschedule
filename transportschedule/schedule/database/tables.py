from sqlalchemy import String, BLOB
from sqlalchemy.orm import Mapped, mapped_column

from transportschedule.schedule.database.connect import Base


class UserRoute(Base):
    __tablename__ = "user_route"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(BLOB)
    thread: Mapped[str] = mapped_column(String(40))
    number: Mapped[str] = mapped_column(String(10))
    from_station: Mapped[str] = mapped_column(String(10))
    to_station: Mapped[str] = mapped_column(String(10))
    salt: Mapped[str] = mapped_column(BLOB)
