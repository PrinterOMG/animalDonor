from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class User(Base):
    __tablename__ = 'user'

    first_name: Mapped[str] = mapped_column(nullable=True)
    second_name: Mapped[str] = mapped_column(nullable=True)
    patronymic: Mapped[str] = mapped_column(nullable=True)

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=True)

    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    city: Mapped[str] = mapped_column(nullable=True)
    avatar: Mapped[str] = mapped_column(nullable=True)
    is_email_public: Mapped[bool] = mapped_column(nullable=True, default=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    phone: Mapped[str] = mapped_column(nullable=True)
    is_email_confirm: Mapped[bool] = mapped_column(nullable=False, default=False)

    telegram_id: Mapped[int] = mapped_column(nullable=True)
