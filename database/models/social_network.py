from datetime import datetime

import sqlalchemy
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class SocialNetwork(Base):
    __tablename__ = 'social_network'

    link: Mapped[str] = mapped_column(nullable=False)
    is_public: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, ForeignKey('user.id'), nullable=False)
    social_network_type_id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, ForeignKey('social_network_type.id'), nullable=False)

    user: Mapped['User'] = relationship('User', backref='social_networks')
    social_network_type: Mapped['SocialNetworkType'] = relationship('SocialNetworkType', backref='social_networks')
