from datetime import datetime, date

import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Pet(Base):
    __tablename__ = 'pet'

    name: Mapped[str] = mapped_column(nullable=True)
    breed: Mapped[str] = mapped_column(nullable=True)
    blood_type: Mapped[str] = mapped_column(nullable=True)
    avatar: Mapped[str] = mapped_column(nullable=True)
    vet_passport: Mapped[str] = mapped_column(nullable=True)
    birthday: Mapped[date] = mapped_column(nullable=True)
    weight: Mapped[float] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(nullable=False)

    owner_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, ForeignKey('user.id'), nullable=False)
    pet_type_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, ForeignKey('pet_type.id'), nullable=False)

    owner: Mapped['User'] = relationship('User', backref='pets')
    pet_type: Mapped['PetType'] = relationship('PetType', backref='pets')

    # Also there are
    # donations, unavailable_lists, vaccinations
