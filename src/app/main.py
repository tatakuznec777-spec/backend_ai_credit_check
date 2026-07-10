from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.v1.router import api_v1_router
from app.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager для startup/shutdown событий.
    """
    print("🚀 Starting Document Checker API...")
    # Здесь можно инициализировать пул БД, кеш и т.д.
    yield
    print("🛑 Shutting down Document Checker API...")
    # Cleanup при остановке


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
)

# Подключаем роутер API v1
app.include_router(api_v1_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    """Root endpoint с информацией об API."""
    return {
        "message": "Document Checker API",
        "docs": "/docs" if settings.debug else "Disabled in production",
        "health": "/api/health",
        "api_v1": "/api/checks",
    }