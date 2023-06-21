from pydantic import BaseSettings, Field


class GoodsConfig(BaseSettings):
    MINIO_ACCESS: str = Field(env="MINIO_ACCESS")
    MINIO_SECRET: str = Field(env="MINIO_SECRET")
    MINIO_HOST: str = Field(env="MINIO_HOST", default="minio")
