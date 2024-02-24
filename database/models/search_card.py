from datetime import datetime, date

import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class SearchCard(Base):
    __tablename__ = 'search_card'

    description: Mapped[str] = mapped_column(nullable=True)
    destination_point: Mapped[str] = mapped_column(nullable=True)
    blood_amount: Mapped[int] = mapped_column(nullable=True)
    active_until: Mapped[date] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)

    author_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, ForeignKey('user.id'), nullable=False)
    recipient_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, ForeignKey('pet.id'), nullable=False)

    author: Mapped['User'] = relationship('User', backref='search_cards')
    recipient: Mapped['Pet'] = relationship('Pet', backref='search_cards')
