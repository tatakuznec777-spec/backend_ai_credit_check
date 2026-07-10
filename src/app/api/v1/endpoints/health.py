from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health", summary="Health check", description="Проверка работоспособности API")
async def health_check():
    """Health check endpoint for Docker и мониторинга."""
    return JSONResponse(
        content={
            "status": "ok",
            "service": "Document Checker API",
            "version": "0.1.0",
        },
        status_code=200,
    )