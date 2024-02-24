import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa

from database.base import Base


class TelegramLinkRequest(Base):
    __tablename__ = 'telegram_link_request'

    key: Mapped[UUID] = mapped_column(unique=True, nullable=False, default=uuid.uuid4)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, sa.ForeignKey('user.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped['User'] = relationship('User')
