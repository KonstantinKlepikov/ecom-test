from fastapi import APIRouter
from app.api.api_v1.endpoints import templ


api_router = APIRouter()

api_router.include_router(
    templ.router, prefix="/templates", tags=['templates', ]
        )
