# type: ignore
import uuid
from typing import Any, Dict, Generic, Optional, Union
from fastapi import Request, Response
from ldap3 import Server, ALL_ATTRIBUTES
import os

from fastapi import Depends
from fastapi_users import (
    InvalidID,
    FastAPIUsers,
    UUIDIDMixin,
    schemas,
    exceptions,
    models,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String

from client_bulksearch.db.base import Base
from client_bulksearch.db.dependencies import get_db_session
from client_bulksearch.settings import settings
from client_bulksearch.ldap_auth import ldap_login, ldap_group

# modifications to fastapi_users code
from client_bulksearch.manager import BaseUserManager

LDAP_HOST = os.getenv("LDAP_HOST")
LDAP_AUTH_FLAG = os.getenv("LDAP_AUTH")
RESTRICTED_GROUP = os.getenv("RESTRICTED_GROUP")


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "appuser"

    username: Mapped[str] = mapped_column(String(length=200))
    """Represents a user entity."""


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str
    """Represents a read command for a user."""


class UserCreate(schemas.BaseUserCreate):
    username: str
    """Represents a create command for a user."""


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    """Represents an update command for a user."""


# use usermanager InvalidID to check against ldap
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """Manages a user session and its tokens."""

    async def on_after_register(
        self, user: models.UP, request: Optional[Request] = None
    ) -> None:
        """
        Perform logic after successful user registration.

        *You should overload this method to add your own logic.*

        :param user: The registered user
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        """

        return  # pragma: no cover

    reset_password_token_secret = settings.users_secret
    verification_token_secret = settings.users_secret


async def get_user_db(
    session: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyUserDatabase:
    """
    Yield a SQLAlchemyUserDatabase instance.

    :param session: asynchronous SQLAlchemy session.
    :yields: instance of SQLAlchemyUserDatabase.
    """
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> UserManager:
    """
    Yield a UserManager instance.

    :param user_db: SQLAlchemy user db instance
    :yields: an instance of UserManager.
    """
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy:
    """
    Return a JWTStrategy in order to instantiate it dynamically.

    :returns: instance of JWTStrategy with provided settings.
    """
    return JWTStrategy(secret=settings.users_secret, lifetime_seconds=None)


cookie_transport = CookieTransport(cookie_max_age=3600)
auth_jwt = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

backends = [
    auth_jwt,
]

# bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
# auth_jwt = AuthenticationBackend(
#     name="jwt",
#     transport=bearer_transport,
#     get_strategy=get_jwt_strategy,
# )

# backends = [
#     auth_jwt,
# ]

api_users = FastAPIUsers[User, uuid.UUID](get_user_manager, backends)

current_active_user = api_users.current_user(active=True)
