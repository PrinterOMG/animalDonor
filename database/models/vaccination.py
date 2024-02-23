from datetime import datetime

import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Vaccination(Base):
    __tablename__ = 'vaccination'

    name: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=True)
    is_approved: Mapped[bool] = mapped_column(nullable=True)
    active_until: Mapped[datetime] = mapped_column(nullable=True)

    pet_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, ForeignKey('pet.id'), nullable=True)

    pet: Mapped['Pet'] = relationship('Pet', backref='vaccination')
