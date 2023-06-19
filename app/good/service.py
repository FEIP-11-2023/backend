import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.good import models
from app.good import exceptions


async def get_brand_by_name(name: str, db: AsyncSession) -> Optional[models.Brand]:
    return (
        await db.execute(select(models.Brand).filter(models.Brand.name == name))
    ).one_or_none()


async def get_brand_by_id(id: uuid.UUID, db: AsyncSession) -> Optional[models.Brand]:
    return (
        await db.execute(select(models.Brand).filter(models.Brand.id == id))
    ).one_or_none()


async def create_brand(name: str, db: AsyncSession):
    brand = await get_brand_by_name(name, db)

    if brand is not None:
        raise exceptions.EntityAlreadyExists

    brand = models.Brand(name=name)
    db.add(brand)
    await db.flush()
    await db.refresh(brand)

    return brand.id


async def update_brand(id: uuid.UUID, name: str, db: AsyncSession):
    brand = await get_brand_by_name(name, db)
    if brand is not None and brand.id != id:
        raise exceptions.EntityAlreadyExists

    brand = await get_brand_by_id(id, db)
    if brand is None:
        raise exceptions.EntityNotFound
    brand.name = name
    await db.commit()