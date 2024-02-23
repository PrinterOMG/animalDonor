from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class User(Base):
    __tablename__ = 'user'

    name: Mapped[str] = mapped_column(nullable=False)
