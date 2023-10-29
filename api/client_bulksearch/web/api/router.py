from fastapi.routing import APIRouter
from fastapi import Depends
import fastapi_users

from client_bulksearch.web.api import dummy, echo, monitoring, redis, users, files

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(users.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
api_router.include_router(redis.router, prefix="/redis", tags=["redis"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
