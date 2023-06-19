from pydantic import BaseSettings, Field
import secrets


class GoodsConfig(BaseSettings):
    MINIO_ACCESS = Field(env="MINIO_ACCESS")
    MINIO_SECRET = Field(env="MINIO_SECRET")
    MINIO_HOST = Field(env="MINIO_HOST")
