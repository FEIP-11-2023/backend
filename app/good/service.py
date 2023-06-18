from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.good import models
from app.good import exceptions


async def create_brand(name: str, db: AsyncSession):
    brand: Optional[models.Brand] = (
        await db.execute(select(models.Brand).filter(models.Brand.name == name))
    ).one_or_none()

    if brand is not None:
        raise exceptions.EntityAlreadyExists

    brand = models.Brand(name=name)
    db.add(brand)
    await db.flush()
    await db.refresh(brand)

    return brand.id
