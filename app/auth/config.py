from pydantic import BaseSettings, Field
import secrets


class AuthConfig(BaseSettings):
    jwt_key = Field(default=secrets.token_hex(128), env="JWT_KEY")
    jwt_algorithm = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expire_minutes = Field(default=30, env="JWT_EXPIRE_MINUTES")
