from datetime import datetime

import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Donation(Base):
    __tablename__ = 'donation'

    is_successful: Mapped[bool] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=True)

    search_card_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, ForeignKey('search_card.id'), nullable=True)
    donor_pet_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, ForeignKey('pet.id'), nullable=True)

    search_card: Mapped['SearchCard'] = relationship('SearchCard', backref='donations')
    donor_pet: Mapped['Pet'] = relationship('Pet', backref='donations')
