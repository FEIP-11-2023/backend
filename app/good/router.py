import uuid
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.good import schemas
import app.good.models as models
from app.auth import dependencies as AuthDeps
from app.auth.models import User as AuthUser
from app.good import service

router = APIRouter()


@router.post(
    "/create_good",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
    response_model=uuid.UUID,
)
async def create_good(
    request: schemas.CreateGood,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pass


@router.patch(
    "/update_good",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
)
async def update_good(
    request: schemas.UpdateGood,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pass


@router.post(
    "/create_brand",
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
    "/update_brand",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
)
async def update_brand(
    request: schemas.UpdateBrand,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await service.update_brand(request.brand_id, request.name, db)


@router.post(
    "/create_category",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
    response_model=uuid.UUID,
)
async def create_category(
    request: schemas.CreateBrand,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pass


@router.patch(
    "/update_category",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
)
async def update_category(
    request: schemas.UpdateCategory,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pass


@router.post(
    "/create_color",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
)
async def create_color(
    request: schemas.CreateColor, db: Annotated[AsyncSession, Depends(get_db)]
):
    pass


@router.patch(
    "/update_color",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
)
async def update_color(
    request: schemas.UpdateBrand, db: Annotated[AsyncSession, Depends(get_db)]
):
    pass


@router.post(
    "/create_sale",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
)
async def create_sale(
    request: schemas.CreateSale, db: Annotated[AsyncSession, Depends(get_db)]
):
    pass


@router.patch(
    "/switch_sale",
    dependencies=[Depends(AuthDeps.admin_required)],
    tags=["goods", "admin"],
)
async def switch_sale(
    request: schemas.SwitchSale, db: Annotated[AsyncSession, Depends(get_db)]
):
    pass
