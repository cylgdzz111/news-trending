from fastapi import APIRouter

from app.api.endpoints import hotsearch, platform

api_router = APIRouter()

api_router.include_router(
    hotsearch.router,
    prefix="/hotsearch",
    tags=["热搜"]
)

api_router.include_router(
    platform.router,
    prefix="/platform",
    tags=["平台"]
) 