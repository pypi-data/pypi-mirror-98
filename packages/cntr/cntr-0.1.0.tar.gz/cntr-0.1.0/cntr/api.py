from fastapi import APIRouter

from cntr.auth.views import user_router, auth_router
from cntr.core.views import items_router, utils_router

api_router = APIRouter()
api_router.include_router(auth_router, tags=["login"])
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(utils_router, prefix="/utils", tags=["utils"])
api_router.include_router(items_router, prefix="/items", tags=["items"])
