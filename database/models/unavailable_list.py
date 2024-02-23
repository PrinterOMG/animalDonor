from datetime import datetime

import sqlalchemy
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class UnavailableList(Base):
    __tablename__ = 'unavailable_list'

    start_at: Mapped[datetime] = mapped_column(nullable=False)
    end_at: Mapped[datetime] = mapped_column(nullable=False)

    pet_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, ForeignKey('pet.id'), nullable=True)

    owner: Mapped['Pet'] = relationship('Pet', backref='unavailable_lists')
