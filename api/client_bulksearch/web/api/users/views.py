from fastapi import APIRouter, Depends

from client_bulksearch.db.models.users import UserCreate  # type: ignore
from client_bulksearch.db.models.users import UserRead  # type: ignore
from client_bulksearch.db.models.users import UserUpdate  # type: ignore
from client_bulksearch.db.models.users import api_users  # type: ignore
from client_bulksearch.db.models.users import get_user_manager

# from client_bulksearch.db.models.users import auth_cookie  # type: ignore
from client_bulksearch.db.models.users import auth_jwt  # type: ignore

# from client_bulksearch.db.models.users import current_active_user

router = APIRouter()

current_superuser = api_users.current_user(superuser=True)


router.include_router(
    api_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(current_superuser)],
)

# router.include_router(
#     api_users.get_register_router(on_after_register),
#     prefix="/auth",
#     tags=["auth"],
#     dependencies=[Depends(current_superuser)],
# )


router.include_router(
    api_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    api_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    api_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
router.include_router(
    api_users.get_auth_router(auth_jwt),
    prefix="/auth/jwt",
    tags=["auth"],
)

# app.include_router(
#     api_users.get_register_router(on_after_register),
#     prefix="/auth",
#     tags=["auth"],
#     dependencies=[Depends(api_users.get_current_superuser)],
# )
