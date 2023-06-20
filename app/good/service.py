import decimal
import uuid
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from app.good import models, schemas
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
    id = brand.id
    await db.commit()

    return id


async def update_brand(id: uuid.UUID, name: str, db: AsyncSession):
    brand = await get_brand_by_name(name, db)
    if brand is not None and brand[0].id != id:
        raise exceptions.EntityAlreadyExists

    brand = await get_brand_by_id(id, db)
    if brand is None:
        raise exceptions.EntityNotFound
    brand[0].name = name
    await db.commit()


async def get_brands(db: AsyncSession) -> List[schemas.Brand]:
    brands = (await db.execute(select(models.Brand))).fetchall()

    return list(map(lambda x: schemas.Brand.from_orm(x[0]), brands))


async def get_color_by_id(id: uuid.UUID, db: AsyncSession) -> Optional[models.Color]:
    return (
        await db.execute(select(models.Color).filter(models.Color.id == id))
    ).one_or_none()


async def get_color_by_name(name: str, db: AsyncSession) -> Optional[models.Color]:
    return (
        await db.execute(select(models.Color).filter(models.Color.name == name))
    ).one_or_none()


async def create_color(name: str, db: AsyncSession) -> uuid.UUID:
    color = await get_color_by_name(name, db)

    if color is not None:
        raise exceptions.EntityAlreadyExists

    color = models.Color(name=name)

    db.add(color)
    await db.flush()
    await db.refresh(color)
    id = color.id
    await db.commit()

    return id


async def update_color(id: uuid.UUID, name: str, db: AsyncSession):
    color_by_name = await get_color_by_name(name, db)

    if color_by_name is not None and color_by_name[0].id != id:
        raise exceptions.EntityAlreadyExists

    color = await get_color_by_id(id, db)

    if color is None:
        raise exceptions.EntityNotFound(str(id))

    print(color)

    color[0].name = name

    await db.commit()


async def get_good_by_id(id: uuid.UUID, db: AsyncSession) -> Optional[models.Good]:
    return (
        await db.execute(
            select(models.Good).with_for_update().filter(models.Good.id == id)
        )
    ).one_or_none()


async def get_sale_by_id(id: uuid.UUID, db: AsyncSession) -> Optional[models.Sale]:
    return (
        await db.execute(
            select(models.Sale).with_for_update().filter(models.Sale.id == id)
        )
    ).one_or_none()


async def get_sales_by_good_id(
    good_id: uuid.UUID, db: AsyncSession
) -> List[models.Sale]:
    good = await get_good_by_id(good_id, db)
    if good is None:
        raise exceptions.EntityNotFound(str(good_id))

    return good.sales


async def create_sale(good_id: uuid.UUID, size: int, db: AsyncSession) -> uuid.UUID:
    current_sales = await get_sales_by_good_id(good_id, db)

    new_sale = models.Sale(good_id=good_id, size=size)

    for sale in current_sales:
        if sale.active:
            new_sale.active = False

    db.add(new_sale)
    await db.flush()
    await db.refresh(new_sale)
    id = new_sale.id
    await db.commit()
    return id


async def switch_sale(sale_id: uuid.UUID, state: bool, db: AsyncSession):
    sale = await get_sale_by_id(sale_id, db)
    if state:
        current_sales = await get_sales_by_good_id(sale.good_id, db)
        for current_sale in current_sales:
            if current_sale.active:
                current_sale.active = False
                break

    sale.active = state

    await db.commit()


async def get_category_by_id(
    id: uuid.UUID, db: AsyncSession
) -> Optional[models.Category]:
    return (
        await db.execute(
            select(models.Category).with_for_update().filter(models.Category.id == id)
        )
    ).one_or_none()


async def get_category_by_name(
    name: str, db: AsyncSession
) -> Optional[models.Category]:
    return (
        await db.execute(
            select(models.Category)
            .with_for_update()
            .filter(models.Category.name == name)
        )
    ).one_or_none()


async def create_category(name: str, db: AsyncSession):
    category = await get_category_by_name(name, db)
    if category is not None:
        raise exceptions.EntityAlreadyExists

    category = models.Category(name=name)

    db.add(category)
    await db.flush()
    await db.refresh(category)
    id = category.id
    await db.commit()

    return id


async def update_category(id: uuid.UUID, name: str, db: AsyncSession):
    category = await get_category_by_name(name, db)
    if category is not None and category[0].id != id:
        raise exceptions.EntityAlreadyExists

    category = await get_category_by_id(id, db)

    if category is None:
        raise exceptions.EntityNotFound(str(id))

    category[0].name = name

    await db.commit()

    return


async def get_categories(db: AsyncSession) -> List[schemas.Category]:
    categories = (await db.execute(select(models.Category))).fetchall()

    return list(map(lambda x: schemas.Category.from_orm(x[0]), categories))


async def get_colors(db: AsyncSession) -> List[schemas.Color]:
    colors = (await db.execute(select(models.Color))).fetchall()

    return list(map(lambda x: schemas.Color.from_orm(x[0]), colors))


async def get_good_by_name(name: str, db: AsyncSession) -> Optional[models.Good]:
    good = (
        await db.execute(
            select(models.Good).with_for_update().filter(models.Good.name == name)
        )
    ).one_or_none()

    if good is None:
        return None

    return good[0]


async def create_good(
    name: str,
    description: str,
    price: decimal.Decimal,
    category_id: uuid.UUID,
    color_id: uuid.UUID,
    brand_id: uuid.UUID,
    db: AsyncSession,
) -> uuid.UUID:
    color = await get_color_by_id(color_id, db)
    if color is None:
        raise exceptions.EntityNotFound(str(color_id))

    brand = await get_brand_by_id(brand_id, db)
    if brand is None:
        raise exceptions.EntityNotFound(str(brand_id))

    category = await get_category_by_id(category_id, db)
    if category is None:
        raise exceptions.EntityNotFound(str(category_id))

    good = await get_good_by_name(name, db)
    if good is not None:
        raise exceptions.EntityAlreadyExists()

    new_good = models.Good(
        name=name,
        description=description,
        color_id=color_id,
        brand_id=brand_id,
        category_id=category_id,
        cost=price,
    )

    db.add(new_good)
    await db.flush()
    await db.refresh(new_good)

    id = new_good.id

    await db.commit()

    return id


async def update_good(
    id: uuid.UUID,
    name: str,
    description: str,
    price: decimal.Decimal,
    category_id: uuid.UUID,
    color_id: uuid.UUID,
    brand_id: uuid.UUID,
    db: AsyncSession,
) -> uuid.UUID:
    color = await get_color_by_id(color_id, db)
    if color is None:
        raise exceptions.EntityNotFound(str(color_id))

    brand = await get_brand_by_id(brand_id, db)
    if brand is None:
        raise exceptions.EntityNotFound(str(brand_id))

    category = await get_category_by_id(category_id, db)
    if category is None:
        raise exceptions.EntityNotFound(str(category_id))

    good = await get_good_by_name(name, db)
    if good is not None and good.id != id:
        raise exceptions.EntityAlreadyExists()

    good = await get_good_by_id(id, db)
    if good is None:
        raise exceptions.EntityNotFound(str(id))

    good.name = name
    good.description = description
    good.cost = price
    good.category_id = category_id
    good.color_id = color_id
    good.brand_id = brand_id

    await db.commit()

    return id


async def get_goods(db: AsyncSession) -> List[schemas.Good]:
    goods = (
        await db.execute(
            select(models.Good).options(
                joinedload(models.Good.color),
                joinedload(models.Good.category),
                joinedload(models.Good.brand),
                joinedload(models.Good.sales),
                joinedload(models.Good.sizes),
                joinedload(models.Good.photos)
            )
        )
    ).scalars()
    
    print(goods)
    
    return list(map(lambda x: schemas.Good.from_orm(x), goods))
