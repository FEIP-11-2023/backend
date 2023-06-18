import enum
from typing import Optional, List

from sqlalchemy import String, ForeignKey, LargeBinary, DateTime, func, Boolean, Enum, UniqueConstraint, NUMERIC
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database import Base, TableNameAndIDMixin


class Brand(Base, TableNameAndIDMixin):
    name: Mapped[str] = mapped_column(unique=True)


class Category(Base, TableNameAndIDMixin):
    name: Mapped[str] = mapped_column(unique=True)


class Color(Base, TableNameAndIDMixin):
    name: Mapped[str] = mapped_column(unique=True)


class Good(Base, TableNameAndIDMixin):
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    category_id: Mapped[UUID] = mapped_column(ForeignKey(Category.id))
    brand_id: Mapped[UUID] = mapped_column(ForeignKey(Brand.id))
    color_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey(Color.id))
    cost: Mapped[NUMERIC] = mapped_column(NUMERIC(10, 2))

    sales: Mapped["Sale"] = relationship("Sale")
    brand: Mapped[Brand] = relationship(Brand)
    category: Mapped[Category] = relationship(Category)
    color: Mapped[Optional[Color]] = relationship(Color)

    sizes: Mapped[List["Size"]] = relationship("Size", back_populates="Size.good")


class Sale(Base, TableNameAndIDMixin):
    good_id: Mapped[UUID] = mapped_column(ForeignKey(Good.id))
    size: Mapped[int]


class Size(Base, TableNameAndIDMixin):
    good_id: Mapped[UUID] = mapped_column(ForeignKey(Good.id))
    size: Mapped[str] = mapped_column()

    UniqueConstraint(good_id, size)

    good: Mapped[Good] = relationship(Good, back_populates=Good.sizes)