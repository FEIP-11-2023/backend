import uuid

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from typing import Generator

from app.config import DBCreds


engine = create_async_engine(DBCreds().get_db_connection_string(), pool_size=30)

SessionLocal = async_sessionmaker(bind=engine)


async def get_db() -> Generator[AsyncSession, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


class Base(DeclarativeBase):
    pass


class TableNameAndIDMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
