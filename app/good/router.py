import uuid
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Form, File, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.good import schemas
import app.good.models as models
from app.auth import dependencies as AuthDeps
from app.auth.models import User as AuthUser
from app.good import service

router = APIRouter()


@router.post(
    "/good",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
    response_model=uuid.UUID,
)
async def create_good(
    request: schemas.CreateGood,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await service.create_good(
        request.name,
        request.description,
        request.price,
        request.category_id,
        request.color_id,
        request.brand_id,
        db,
    )


@router.patch(
    "/good",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
)
async def update_good(
    request: schemas.UpdateGood,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await service.update_good(
        request.good_id,
        request.name,
        request.description,
        request.price,
        request.category_id,
        request.color_id,
        request.brand_id,
        db,
    )


@router.delete(
    "/good", dependencies=[Depends(AuthDeps.admin_required)], tags=["goods", "admin"]
)
async def delete_good(good_id: uuid.UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    return await service.delete_good_id(good_id, db)


@router.post(
    "/good/photo",
    tags=["goods", "admin"],
    dependencies=[Depends(AuthDeps.admin_required)],
    response_model=uuid.UUID,
)
async def add_good_photo(
    good_id: Annotated[uuid.UUID, Form()],
    photo: Annotated[UploadFile, File()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await service.add_photo(
        good_id, await photo.read(), photo.filename.split(".")[-1], db
    )


@router.get("/good/all", tags=["goods", "admin"], response_model=List[schemas.Good])
async def get_all_goods(db: Annotated[AsyncSession, Depends(get_db)]):
    return await service.get_goods(db)


@router.post(
    "/brand",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
    response_model=uuid.UUID,
)
async def create_brand(
    request: schemas.CreateBrand,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await service.create_brand(request.name, db)


@router.patch(
    "/brand",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
)
async def update_brand(
    request: schemas.UpdateBrand,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await service.update_brand(request.brand_id, request.name, db)


@router.get("/brand", tags=["goods"], response_model=List[schemas.Brand])
async def get_brands(db: Annotated[AsyncSession, Depends(get_db)]):
    return await service.get_brands(db)


@router.post(
    "/category",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
    response_model=uuid.UUID,
)
async def create_category(
    request: schemas.CreateCategory,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await service.create_category(request.name, db)


@router.patch(
    "/category",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
)
async def update_category(
    request: schemas.UpdateCategory,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await service.update_category(request.category_id, request.name, db)


@router.patch(
    "/category/photo",
    tags=["goods", "admin"],
    dependencies=[Depends(AuthDeps.admin_required)],
    response_model=uuid.UUID,
)
async def add_good_photo(
    category_id: Annotated[uuid.UUID, Form()],
    photo: Annotated[UploadFile, File()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await service.set_category_photo(
        category_id, await photo.read(), photo.filename.split(".")[-1], db
    )


@router.get("/good/search", tags=["goods"], response_model=List[schemas.Good])
async def search_goods(
    db: Annotated[AsyncSession, Depends(get_db)],
    name: Annotated[Optional[str], Query()] = "",
    brand_ids: Annotated[Optional[List[uuid.UUID]], Query()] = [],
    color_ids: Annotated[Optional[List[uuid.UUID]], Query()] = [],
    category_ids: Annotated[Optional[List[uuid.UUID]], Query()] = [],
    limit: Annotated[Optional[int], Query()] = 10,
    offset: Annotated[Optional[int], Query()] = 0,
):
    return await service.search_goods(
        name, brand_ids, color_ids, category_ids, limit, offset, db
    )


@router.get("/category", tags=["goods"], response_model=List[schemas.Category])
async def get_categories(db: Annotated[AsyncSession, Depends(get_db)]):
    return await service.get_categories(db)


@router.post(
    "/color",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
)
async def create_color(
    request: schemas.CreateColor, db: Annotated[AsyncSession, Depends(get_db)]
):
    return await service.create_color(request.name, db)


@router.patch(
    "/color",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
)
async def update_color(
    request: schemas.UpdateColor, db: Annotated[AsyncSession, Depends(get_db)]
):
    return await service.update_color(request.color_id, request.name, db)


@router.get("/color", tags=["goods", "user"], response_model=List[schemas.Color])
async def get_colors(db: Annotated[AsyncSession, Depends(get_db)]):
    return await service.get_colors(db)


@router.post(
    "/sale",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
)
async def create_sale(
    request: schemas.CreateSale, db: Annotated[AsyncSession, Depends(get_db)]
):
    return await service.create_sale(request.good_id, request.size, db)


@router.patch(
    "/switch_sale",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
)
async def switch_sale(
    request: schemas.SwitchSale, db: Annotated[AsyncSession, Depends(get_db)]
):
    return await service.switch_sale(
        sale_id=request.sale_id, state=request.active, db=db
    )


@router.get(
    "/get_sales",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
    response_model=List[schemas.Sale],
)
async def get_sales(good_id: uuid.UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    return await service.get_sales_by_good_id(good_id, db)


@router.post("/cart", tags=["goods"], response_model=uuid.UUID)
async def add_to_cart(
    request: schemas.AddToCartRequest,
    user: Annotated[AuthUser, Depends(AuthDeps.user_by_token(login_required=True))],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await service.add_to_cart(
        user.id, request.good_id, request.size_id, request.count, db
    )


@router.post(
    "/size",
    tags=["admin", "goods"],
    dependencies=[Depends(AuthDeps.admin_required)],
    response_model=uuid.UUID,
)
async def create_size(
    request: schemas.CreateSize, db: Annotated[AsyncSession, Depends(get_db)]
):
    return await service.create_size(
        request.good_id, request.size, request.remainder, db
    )


@router.post(
    "/size/set",
    tags=["admin", "goods"],
    dependencies=[Depends(AuthDeps.admin_required)],
)
async def set_remainder(
    request: schemas.SetSizeRemainder, db: Annotated[AsyncSession, Depends(get_db)]
):
    await service.set_size_count(request.size_id, request.remainder, db)


@router.delete("/cart", tags=["goods"], response_model=uuid.UUID)
async def delete_from_cart(
    request: schemas.DeleteFromCartRequest,
    user: Annotated[AuthUser, Depends(AuthDeps.user_by_token(login_required=True))],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await service.delete_from_cart(user.id, request.size_id, db)


@router.get("/cart", tags=["goods"], response_model=List[schemas.Cart])
async def get_cart(
    user: Annotated[AuthUser, Depends(AuthDeps.user_by_token(login_required=True))],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await service.get_cart(user.id, db)
