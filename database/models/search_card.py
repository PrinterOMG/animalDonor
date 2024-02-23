from datetime import datetime

import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class SearchCard(Base):
    __tablename__ = 'search_card'

    description: Mapped[str] = mapped_column(nullable=True)
    destination_point: Mapped[str] = mapped_column(nullable=True)
    blood_amount: Mapped[int] = mapped_column(nullable=True)
    active_until: Mapped[datetime] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=True)

    author_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, ForeignKey('user.id'), nullable=True)
    recipient_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, ForeignKey('pet.id'), nullable=True)

    author: Mapped['User'] = relationship('User', backref='search_cards')
    recipient: Mapped['Pet'] = relationship('Pet', backref='search_cards')
