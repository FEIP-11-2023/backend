from pydantic import BaseSettings, Field


class DBCreds(BaseSettings):
    db_username: str = Field(env="DB_USERNAME")
    db_password: str = Field(env="DB_PASSWORD")
    db_host: str = Field(env="DB_HOST")
    db: str = Field(default="carve", env="DB_DATABASE")

    def get_db_connection_string(self):
        return f"postgresql+asyncpg://{self.db_username}:{self.db_password}@{self.db_host}/{self.db}"

    def get_sync_db_connection_string(self):
        return f"postgresql+psycopg2://{self.db_username}:{self.db_password}@{self.db_host}/{self.db}"
