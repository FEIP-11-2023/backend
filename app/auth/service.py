import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import models, exceptions


async def create_user(username: str, password: str, email: str, db: AsyncSession):
    # region Check that user with such username and password does not exist
    user_by_login, user_by_email = (
        await db.execute(select(models.User).filter(models.User.username == username)),
        await db.execute(select(models.User).filter(models.User.email == email)),
    )

    user_by_login, user_by_email = (
        user_by_login.one_or_none(),
        user_by_email.one_or_none(),
    )

    if user_by_login is not None:
        raise exceptions.UsernameAlreadyExists

    if user_by_email is not None:
        raise exceptions.EmailAlreadyExists
    # endregion

    # region Create new user

    user = models.User(
        username=username,
        email=email,
        role=models.Role.admin,
        password_hash=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()),
    )

    db.add(user)

    # endregion

    await db.commit()

    return
