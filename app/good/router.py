from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.good import schemas
from app.auth import dependencies as AuthDeps
from app.auth.models import User as AuthUser

router = APIRouter()


@router.post("/create_good", dependencies=[Depends(AuthDeps.admin_required)], tags=["goods", "admin"])
async def create_good(
    request: schemas.CreateGood,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pass


@router.patch("/update_good", dependencies=[Depends(AuthDeps.admin_required)], tags=["goods", "admin"])
async def update_good(
    request: schemas.UpdateGood,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pass


@router.post("/create_brand", dependencies=[Depends(AuthDeps.admin_required)], tags=["goods", "admin"])
async def create_brand(
    request: schemas.CreateBrand,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pass


@router.patch("/update_brand", dependencies=[Depends(AuthDeps.admin_required)], tags=["goods", "admin"])
async def update_brand(
    request: schemas.UpdateBrand,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pass


@router.post("/create_category", dependencies=[Depends(AuthDeps.admin_required)], tags=["goods", "admin"])
async def create_category(
    request: schemas.CreateBrand,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pass


@router.patch("/update_category", dependencies=[Depends(AuthDeps.admin_required)], tags=["goods", "admin"])
async def update_category(
    request: schemas.UpdateCategory,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pass
