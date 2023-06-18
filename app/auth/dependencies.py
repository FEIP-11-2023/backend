from functools import wraps
from typing import Type, Callable, Annotated, Optional, Any, Coroutine

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import exceptions
from app.auth.models import User
from app.auth.config import AuthConfig
from app.auth import models
import uuid

from fastapi import Depends

from jose import jwt

from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=False)


def user_by_token(
    extended_class: Type[User] = User, login_required: bool = True
) -> Callable[[str, AsyncSession], Coroutine[Any, Any, Any | None]]:
    async def closure(
        token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
    ):
        if token is None:
            if login_required:
                raise exceptions.Unauthorized()
            else:
                return None
        try:
            token_data = jwt.decode(
                token, AuthConfig().jwt_key, algorithms=[AuthConfig().jwt_algorithm]
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.TokenExpired()
        except jwt.JWTError:
            raise exceptions.Unauthorized()
        except Exception:
            raise exceptions.Unauthorized()

        user = (
            await db.execute(
                select(extended_class)
                .filter(extended_class.id == uuid.UUID(token_data.get("id")))
                .limit(1)
            )
        ).one()[0]

        return user

    return closure


def auth_required(func):
    @wraps(func)
    async def wrapper(_: User = Depends(user_by_token()), *args, **kwargs):
        return await func(*args, **kwargs)

    return wrapper


async def admin_required(user: User = Depends(user_by_token()), *args, **kwargs):
    if user.role != models.Role.admin:
        raise exceptions.PermissionDenied
