from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.good import schemas
from app.auth import dependencies as AuthDeps
from app.auth.models import User as AuthUser

router = APIRouter()


@router.post("/create_good")
async def create_good(
    request: Annotated[schemas.CreateGood, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AuthUser, Depends(AuthDeps.admin_required)],
):
    pass


@router.patch("/update_good")
async def update_good(
    request: Annotated[schemas.UpdateGood, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AuthUser, Depends(AuthDeps.admin_required)],
):
    pass


@router.post("/create_brand")
async def create_brand(
    request: Annotated[schemas.CreateBrand, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AuthUser, Depends(AuthDeps.admin_required)],
):
    pass


@router.patch("/update_brand")
async def update_brand(
    request: Annotated[schemas.UpdateBrand, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AuthUser, Depends(AuthDeps.admin_required)],
):
    pass


@router.post("/create_category")
async def create_category(
    request: Annotated[schemas.CreateBrand, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AuthUser, Depends(AuthDeps.admin_required)],
):
    pass


@router.patch("/update_category")
async def update_category(
    request: Annotated[schemas.UpdateCategory, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
    _: Annotated[AuthUser, Depends(AuthDeps.admin_required)],
):
    pass
