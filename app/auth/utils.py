import datetime

from jose import jwt

from app.auth import models
from app.auth.config import AuthConfig


def get_jwt_for_user(
    user: models.User, timedelta: datetime.timedelta = datetime.timedelta(days=2)
) -> str:
    return jwt.encode(
        {
            "exp": datetime.datetime.now() + timedelta,
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": str(user.role),
        },
        AuthConfig().jwt_key,
        algorithm=AuthConfig().jwt_algorithm,
    )
