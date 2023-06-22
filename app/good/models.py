import enum
import uuid
from typing import Optional, List

from sqlalchemy import (
    String,
    ForeignKey,
    LargeBinary,
    DateTime,
    func,
    Boolean,
    Enum,
    UniqueConstraint,
    NUMERIC,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database import Base, TableNameAndIDMixin, CreatedAtMixin, UpdatedAtMixin


class Brand(Base, TableNameAndIDMixin):
    name: Mapped[str] = mapped_column(unique=True)


class Category(Base, TableNameAndIDMixin):
    name: Mapped[str] = mapped_column(unique=True)

    photo: Mapped[Optional[List["CategoryPhoto"]]] = relationship("CategoryPhoto")


class Color(Base, TableNameAndIDMixin):
    name: Mapped[str] = mapped_column(unique=True)


class Good(Base, TableNameAndIDMixin, CreatedAtMixin, UpdatedAtMixin):
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    category_id: Mapped[UUID] = mapped_column(ForeignKey(Category.id))
    brand_id: Mapped[UUID] = mapped_column(ForeignKey(Brand.id))
    color_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey(Color.id))
    cost: Mapped[NUMERIC] = mapped_column(NUMERIC(10, 2))

    sales: Mapped[List["Sale"]] = relationship("Sale")
    brand: Mapped[Brand] = relationship(Brand)
    category: Mapped[Category] = relationship(Category)
    color: Mapped[Optional[Color]] = relationship(Color)

    sizes: Mapped[List["Size"]] = relationship("Size", back_populates="good")
    photos: Mapped[List["GoodPhoto"]] = relationship("GoodPhoto")


class Sale(Base, TableNameAndIDMixin, CreatedAtMixin, UpdatedAtMixin):
    good_id: Mapped[UUID] = mapped_column(ForeignKey(Good.id))
    size: Mapped[int]
    active: Mapped[bool] = mapped_column(default=True)


class Size(Base, TableNameAndIDMixin):
    good_id: Mapped[UUID] = mapped_column(ForeignKey(Good.id))
    size: Mapped[str] = mapped_column()
    remainder: Mapped[int]

    UniqueConstraint(good_id, size)

    good: Mapped[Good] = relationship("Good", back_populates="sizes")


class GoodPhoto(Base, TableNameAndIDMixin, CreatedAtMixin):
    good_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(Good.id))
    bucket_name: Mapped[str] = mapped_column(default="good-photos")
    image_name: Mapped[str]


class CategoryPhoto(Base, TableNameAndIDMixin):
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(Category.id), unique=True)
    bucket_name: Mapped[str] = mapped_column(default="good-photos")
    image_name: Mapped[str]
