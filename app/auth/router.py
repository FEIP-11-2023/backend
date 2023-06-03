# creates fastapi router for authentication
import datetime
import secrets
from typing import Optional, Annotated, Tuple, List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import app.auth.dependencies as deps

import app.auth.schemas as schemas
from app.auth import models, exceptions, service
from app.auth.utils import get_jwt_for_user

from app.auth.models import User
from app.database import get_db
from app.pay.utils import provide_wallet

import bcrypt

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

SECRET_KEY = "7a50bb01bd42460c6ffafe4afeec16918e088a43d70dbbf0b1f9fb753778ad38"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/register")
async def register(request: schemas.RegisterRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    await service.create_user(
        request.username,
        request.password,
        request.email,
        db
    )
    return


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user: Optional[Tuple[models.User]] = (
        await db.execute(select(models.User).filter(models.User.username == form_data.username))
    ).one_or_none()

    if user is None:
        raise exceptions.InvalidCredentialsException()
    user: models.User = user[0]
    if user.blocked:
        raise exceptions.UserBlocked
    if not bcrypt.checkpw(form_data.password.encode('utf-8'), user.password_hash):
        raise exceptions.InvalidCredentialsException()

    token = get_jwt_for_user(user)

    refresh_token_data = secrets.token_hex(64)
    refresh_token = models.RefreshToken(
        user_id=user.id,
        token=refresh_token_data,
        valid_till=datetime.datetime.utcnow() + datetime.timedelta(30),
    )

    db.add(refresh_token)
    await db.flush()
    await db.commit()

    return {
        "access_token": token,
        "token_type": "bearer",
        "refresh_token": refresh_token_data,
    }


@router.post("/refresh")
async def refresh(token: schemas.RefreshToken, db: AsyncSession = Depends(get_db)):
    token_query = await db.execute(select(models.RefreshToken).filter(models.RefreshToken.token == token.token))
    token_from_db: Optional[List[models.RefreshToken]] = token_query.one_or_none()

    if token_from_db is None:
        raise exceptions.RefreshTokenNotFound
    token_from_db: models.RefreshToken = token_from_db[0]
    if token_from_db.valid_till <= datetime.datetime.utcnow() or token_from_db.revoked:
        raise exceptions.RefreshTokenExpiredOrRevoked

    token_from_db.revoked = True
    refresh_token_data = secrets.token_hex(64)
    refresh_token = models.RefreshToken(
        user_id=token_from_db.user_id,
        token=refresh_token_data,
        valid_till=datetime.datetime.utcnow() + datetime.timedelta(30),
    )
    db.add(refresh_token)

    await db.flush()

    new_jwt_token = get_jwt_for_user(refresh_token.user)
    
    await db.commit()

    return {
        "access_token": new_jwt_token,
        "token_type": "bearer",
        "refresh_token": refresh_token_data,
    }


@router.get("/get_user")
async def get_user(user: User = Depends(deps.user_by_token(User, login_required=True))):
    return user


@router.get("/get_user_optional")
async def get_user(user: User = Depends(deps.user_by_token(User, login_required=False))):
    return user
