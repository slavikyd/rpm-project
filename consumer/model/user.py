from sqlalchemy.orm import Mapped, mapped_column

from .db_main import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(index=True)
    age: Mapped[int]
    gender: Mapped[str]
    description: Mapped[str]
    filter_by_age: Mapped[str]
    filter_by_gender: Mapped[str]
    filter_by_description: Mapped[str]    
