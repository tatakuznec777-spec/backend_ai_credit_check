from fastapi import APIRouter

from app.api.v1.endpoints import checks, health

# Создаём роутер для API v1
api_v1_router = APIRouter()

# Подключаем endpoints
api_v1_router.include_router(checks.router, prefix="/checks", tags=["Checks"])
api_v1_router.include_router(health.router, tags=["Health"])