from __future__ import annotations
from typing import Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import event
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel

_engine: Optional[AsyncEngine] = None
SessionLocal: async_sessionmaker[AsyncSession] | None = None

async def init_db(database_url: str) -> None:
    global _engine, SessionLocal

    if _engine is not None:
        return

    _engine = create_async_engine(
        database_url,
        echo=False,
        poolclass=NullPool,
        future=True
    )

    @event.listens_for(_engine.sync_engine, "connect")
    def _sqlite_pragmas(dbapi_conn, _):
        cur = dbapi_conn.cursor()
        cur.execute("PRAGMA journal_mode=WAL;")
        cur.execute("PRAGMA busy_timeout=5000;")
        cur.execute("PRAGMA synchronous=NORMAL;")
        cur.execute("PRAGMA foreign_keys=ON;")
        cur.close()

    SessionLocal = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    SessionLocal = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False
    )

    from mailhook_worker import models #noqa: F401

    async with _engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

def get_engine() -> AsyncEngine:
    if _engine is None:
        raise RuntimeError('init_db() ainda não foi chamado.')

    return _engine

def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    if SessionLocal is None:
        raise RuntimeError('init_db() ainda não foi chamado.')

    return SessionLocal

