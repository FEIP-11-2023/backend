import enum
from typing import Optional, List

from sqlalchemy import String, ForeignKey, LargeBinary, DateTime, func, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database import Base, TableNameAndIDMixin


class Role(enum.Enum):
    guest = 0
    admin = 1


class User(Base, TableNameAndIDMixin):
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

    password_hash: Mapped[LargeBinary] = mapped_column(LargeBinary(64), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.guest, nullable=False)

    blocked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(back_populates='user')

class RefreshToken(Base, TableNameAndIDMixin):
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped[User] = relationship(back_populates='refresh_tokens', lazy='joined')
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    valid_till: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
