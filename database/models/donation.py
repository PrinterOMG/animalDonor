from datetime import datetime

import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Donation(Base):
    __tablename__ = 'donation'

    is_successful: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)

    search_card_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, ForeignKey('search_card.id'), nullable=False)
    donor_pet_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, ForeignKey('pet.id'), nullable=False)

    search_card: Mapped['SearchCard'] = relationship('SearchCard', backref='donations')
    donor_pet: Mapped['Pet'] = relationship('Pet', backref='donations')
