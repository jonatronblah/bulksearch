from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends
from typing import AsyncGenerator
from fastapi_users.exceptions import UserAlreadyExists
import contextlib
import asyncio

from client_bulksearch.settings import settings
from client_bulksearch.db.models.users import UserCreate
from client_bulksearch.db.models.users import get_user_manager, get_user_db


db_url = make_url(str(settings.db_url))
engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    email: str, password: str, username: str, is_superuser: bool = False
):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            username=username,
                            is_superuser=is_superuser,
                        ),
                        ldap_auth=False
                    )
                    print(f"User created {user}")
    except UserAlreadyExists:
        print(f"User {email} already exists")


def run_super():
    asyncio.run(
        create_user(
            email="user@company.com",
            password="password",
            username="user",
            is_superuser=True,
        )
    )
