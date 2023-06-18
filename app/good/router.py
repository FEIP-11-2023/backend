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
    request: Annotated[schemas.CreateGood, Depends(schemas.CreateGood)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pass


@router.patch("/update_good", dependencies=[Depends(AuthDeps.admin_required)], tags=["goods", "admin"])
async def update_good(
    request: Annotated[schemas.UpdateGood, Depends(schemas.UpdateGood)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pass


@router.post("/create_brand", dependencies=[Depends(AuthDeps.admin_required)], tags=["goods", "admin"])
async def create_brand(
    request: Annotated[schemas.CreateBrand, Depends(schemas.CreateBrand)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pass


@router.patch("/update_brand", dependencies=[Depends(AuthDeps.admin_required)], tags=["goods", "admin"])
async def update_brand(
    request: Annotated[schemas.UpdateBrand, Depends(schemas.UpdateBrand)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pass


@router.post("/create_category", dependencies=[Depends(AuthDeps.admin_required)], tags=["goods", "admin"])
async def create_category(
    request: Annotated[schemas.CreateBrand, Depends(schemas.CreateBrand)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pass


@router.patch("/update_category", dependencies=[Depends(AuthDeps.admin_required)], tags=["goods", "admin"])
async def update_category(
    request: Annotated[schemas.UpdateCategory, Depends(schemas.UpdateCategory)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pass
