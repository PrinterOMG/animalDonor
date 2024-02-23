from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class SocialNetworkType(Base):
    __tablename__ = 'social_network_type'

    name: Mapped[str] = mapped_column(nullable=False)
