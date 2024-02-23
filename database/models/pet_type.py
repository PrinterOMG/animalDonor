from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class PetType(Base):
    __tablename__ = 'pet_type'

    name: Mapped[str] = mapped_column(nullable=False)
