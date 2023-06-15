import re
from typing import Optional

from app.auth import models
from app.models import ORJSONModel
from pydantic import validator


class RegisterRequest(ORJSONModel):
    username: str
    password: str
    email: str
    invite_code: Optional[str]

    @validator("password")
    def validate_password(cls, password, **kwargs):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        # check for password complexity
        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(regex, password):
            raise ValueError(
                "Password must contain at least one uppercase letter, one lowercase letter, one number and one special character"
            )
        return password

    @validator("email")
    def validate_email(cls, email, **kwargs):
        if not re.match(r"[^@.+]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email")
        return email


class RefreshToken(ORJSONModel):
    token: str


class User(ORJSONModel):
    username: str
    email: str
    role: models.Role
    blocked: bool

    class Config:
        orm_mode = True
