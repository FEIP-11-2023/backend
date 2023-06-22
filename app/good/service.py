import decimal
import io
import secrets
import uuid
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload, joinedload

from app.good import models, schemas
from app.good import exceptions
from app.good.config import GoodsConfig

import minio


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
        (
            await db.execute(
                select(models.Good)
                .options(selectinload(models.Good.sizes))
                .with_for_update()
                .filter(models.Good.id == id)
            )
        )
        .scalars()
        .one_or_none()
    )


async def get_sale_by_id(id: uuid.UUID, db: AsyncSession) -> Optional[models.Sale]:
    return (
        (
            await db.execute(
                select(models.Sale).with_for_update().filter(models.Sale.id == id)
            )
        )
        .scalars()
        .one_or_none()
    )


async def get_sales_by_good_id(
    good_id: uuid.UUID, db: AsyncSession
) -> List[schemas.Sale]:
    good = (
        (
            await db.execute(
                select(models.Good)
                .with_for_update()
                .options(selectinload(models.Good.sales))
                .filter(models.Good.id == good_id)
            )
        )
        .scalars()
        .one_or_none()
    )
    if good is None:
        raise exceptions.EntityNotFound(str(good_id))

    return list(map(schemas.Sale.from_orm, good.sales))


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
        (
            await db.execute(
                select(models.Category)
                .with_for_update()
                .options(selectinload(models.Category.photo))
                .filter(models.Category.id == id)
            )
        )
        .scalars()
        .one_or_none()
    )


async def get_category_by_name(
    name: str, db: AsyncSession
) -> Optional[models.Category]:
    return (
        (
            await db.execute(
                select(models.Category)
                .with_for_update()
                .options(selectinload(models.Category.photo))
                .filter(models.Category.name == name)
            )
        )
        .scalars()
        .one_or_none()
    )


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
    if category is not None and category.id != id:
        raise exceptions.EntityAlreadyExists

    category = await get_category_by_id(id, db)

    if category is None:
        raise exceptions.EntityNotFound(str(id))

    category.name = name

    await db.commit()

    return


async def get_categories(db: AsyncSession) -> List[schemas.Category]:
    categories = (
        await db.execute(
            select(models.Category).options(selectinload(models.Category.photo))
        )
    ).fetchall()

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
                selectinload(models.Good.color),
                selectinload(models.Good.category).selectinload(models.Category.photo),
                selectinload(models.Good.brand),
                selectinload(models.Good.sales),
                selectinload(models.Good.sizes),
                selectinload(models.Good.photos),
            )
        )
    ).scalars()

    return list(map(lambda x: schemas.Good.from_orm(x), goods))


async def add_photo(
    good_id: uuid.UUID, photo: bytes, extension: str, db: AsyncSession
) -> uuid.UUID:
    good = await get_good_by_id(good_id, db)

    if good is None:
        raise exceptions.EntityNotFound(str(good_id))

    name = secrets.token_hex(30) + "." + extension

    mc = minio.Minio(
        GoodsConfig().MINIO_HOST,
        access_key=GoodsConfig().MINIO_ACCESS,
        secret_key=GoodsConfig().MINIO_SECRET,
        secure=False,
    )

    if not mc.bucket_exists("good-photos"):
        mc.make_bucket("good-photos")

    mc.put_object("good-photos", name, io.BytesIO(photo), len(photo))

    new_photo = models.GoodPhoto(
        good_id=good_id, bucket_name="good-photos", image_name=name
    )

    db.add(new_photo)
    await db.flush()
    await db.refresh(new_photo)

    id = new_photo.id

    await db.commit()

    return id


async def set_category_photo(
    category_id: uuid.UUID, photo: bytes, extension: str, db: AsyncSession
) -> uuid.UUID:
    category = await get_category_by_id(category_id, db)

    if category is None:
        raise exceptions.EntityNotFound(str(category_id))

    name = secrets.token_hex(30) + "." + extension

    mc = minio.Minio(
        GoodsConfig().MINIO_HOST,
        access_key=GoodsConfig().MINIO_ACCESS,
        secret_key=GoodsConfig().MINIO_SECRET,
        secure=False,
    )

    if not mc.bucket_exists("category-photos"):
        mc.make_bucket("category-photos")

    mc.put_object("category-photos", name, io.BytesIO(photo), len(photo))

    if category.photo is not None:
        photo = category.photo
    else:
        photo = models.CategoryPhoto(
            category_id=category_id, bucket_name="category-photos", image_name=name
        )
        db.add(photo)
    await db.flush()
    await db.refresh(photo)

    id = photo.id

    await db.commit()

    return id


async def search_goods(
    name: Optional[str],
    brands: List[uuid.UUID],
    colors: List[uuid.UUID],
    categories: List[uuid.UUID],
    limit: int,
    offset: int,
    db: AsyncSession,
) -> List[schemas.Good]:
    goods = (
        (
            await db.execute(
                select(models.Good)
                .options(
                    selectinload(models.Good.color),
                    selectinload(models.Good.category).selectinload(
                        models.Category.photo
                    ),
                    selectinload(models.Good.brand),
                    selectinload(models.Good.sales),
                    selectinload(models.Good.sizes),
                    selectinload(models.Good.photos),
                )
                .filter(
                    *[
                        models.Good.brand_id.in_(brands) if len(brands) > 0 else True,
                        models.Good.color_id.in_(colors) if len(colors) > 0 else True,
                        models.Good.category_id.in_(categories)
                        if len(categories) > 0
                        else True,
                        models.Good.name.ilike(f"%{name}%") if len(name) > 0 else True,
                    ]
                )
                .offset(offset)
                .limit(limit)
            )
        )
        .scalars()
        .all()
    )

    return list(map(lambda x: schemas.Good.from_orm(x), goods))


async def get_cart_by_user_size(
    user_id: uuid.UUID, size_id: uuid.UUID, db: AsyncSession
) -> Optional[models.Cart]:
    cart = (
        (
            await db.execute(
                select(models.Cart).filter(
                    models.Cart.user_id == user_id, models.Cart.size_id == size_id
                )
            )
        )
        .scalars()
        .one_or_none()
    )

    return cart


async def add_to_cart(
    user_id: uuid.UUID,
    good_id: uuid.UUID,
    size_id: Optional[uuid.UUID],
    count: int,
    db: AsyncSession,
) -> uuid.UUID:
    good = await get_good_by_id(good_id, db)

    if good is None:
        raise exceptions.EntityNotFound(str(good_id))

    if len(good.sizes) != 0:
        if size_id is None:
            raise exceptions.SizeIsRequired
        no_size = True

        for size in good.sizes:
            if size.id == size_id:
                no_size = False
                break

        if no_size:
            raise exceptions.EntityNotFound(str(size_id))
    else:
        raise exceptions.EntityNotFound(str(size_id))

    cart = await get_cart_by_user_size(user_id, size_id, db)

    if cart is None:
        new_cart = models.Cart(
            good_id=good_id, size_id=size_id, count=count, user_id=user_id
        )

        db.add(new_cart)
        await db.flush()
        await db.refresh(new_cart)

        id = new_cart.id

        await db.commit()

        return id
    else:
        cart.count += count

        id = cart.id

        await db.commit()

        return id


async def delete_from_cart(
    user_id: uuid.UUID,
    size_id: Optional[uuid.UUID],
    db: AsyncSession,
):
    cart = await get_cart_by_user_size(user_id, size_id, db)

    if cart is None:
        raise exceptions.EntityNotFound(f"{str(size_id), str(user_id)}")
    else:
        cart.count -= 1

        if cart.count == 0:
            await db.execute(delete(models.Cart).filter(models.Cart.id == cart.id))

        await db.commit()


async def get_size_by_good_id_and_size(
    good_id: uuid.UUID, size: int, db: AsyncSession
) -> Optional[models.Size]:
    size = (
        (
            await db.execute(
                select(models.Size)
                .filter(models.Size.good_id == good_id, models.Size.size == size)
                .with_for_update()
            )
        )
        .scalars()
        .one_or_none()
    )

    return size


async def get_size_by_id(id: uuid.UUID, db: AsyncSession) -> Optional[models.Size]:
    size = (
        (
            await db.execute(
                select(models.Size).filter(models.Size.id == id).with_for_update()
            )
        )
        .scalars()
        .one_or_none()
    )

    return size


async def create_size(
    good_id: uuid.UUID, size: int, remainder: int, db: AsyncSession
) -> uuid.UUID:
    size_ = await get_size_by_good_id_and_size(good_id, size, db)

    if size_ is not None:
        raise exceptions.DuplicateSize

    good = await get_good_by_id(good_id, db)

    if good is None:
        raise exceptions.EntityNotFound(str(good_id))

    new_size = models.Size(good_id=good_id, size=size, remainder=remainder)

    db.add(new_size)
    await db.flush()
    await db.refresh(new_size)

    id = new_size.id

    await db.commit()

    return id


async def set_size_count(size_id: uuid.UUID, remainder: int, db: AsyncSession):
    size = await get_size_by_id(size_id, db)

    if size is None:
        raise exceptions.EntityNotFound(str(size_id))

    size.remainder = remainder

    await db.commit()

    return


async def get_cart(user_id: uuid.UUID, db: AsyncSession) -> List[schemas.Cart]:
    carts = (
        (await db.execute(select(models.Cart).filter(models.Cart.user_id == user_id)))
        .scalars()
        .fetchall()
    )

    return list(map(schemas.Cart.from_orm, carts))
