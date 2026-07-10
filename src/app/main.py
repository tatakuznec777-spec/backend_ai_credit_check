from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup/shutdown events.
    Replace print with proper logging later.
    """
    print("Starting Document Checker API...")
    yield
    print("Shutting down Document Checker API...")


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)


@app.get("/health")
async def health_check():
    """Health check endpoint for Docker and monitoring."""
    return JSONResponse(
        content={
            "status": "ok",
            "service": settings.app_name,
            "version": "0.1.0",
        },
        status_code=200,
    )


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Document Checker API",
        "docs": "/docs" if settings.debug else "Disabled in production",
        "health": "/health",
    }