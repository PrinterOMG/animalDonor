from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class ServiceToken(Base):
    __tablename__ = '__tablename__'

    name: Mapped[str] = mapped_column(nullable=False)
    token: Mapped[UUID] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
