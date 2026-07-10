import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.common.enums import DocumentType, IssueLevel, ProgramType


class IssueSchema(BaseModel):
    """Схема проблемы (ошибка или предупреждение)."""
    level: IssueLevel
    message: str


class DocumentSchema(BaseModel):
    """Схема документа в ответе."""
    name: str = Field(..., description="Имя файла")
    detected_type: Optional[str] = Field(None, description="Определённый тип документа")
    size_kb: int = Field(..., description="Размер файла в КБ")


class ExtractedDataSchema(BaseModel):
    """Схема извлечённых данных из документов."""
    contractor: Optional[str] = Field(None, description="Контрагент")
    amount: Optional[str] = Field(None, description="Сумма")
    date: Optional[str] = Field(None, description="Дата")
    subject: Optional[str] = Field(None, description="Предмет договора")


class CheckResponse(BaseModel):
    """Полный ответ по проверке (POST /api/checks и GET /api/checks/{id})."""
    check_id: uuid.UUID
    status: str
    status_label: str
    reason: Optional[str] = None
    issues: list[IssueSchema] = Field(default_factory=list)
    documents: list[DocumentSchema] = Field(default_factory=list)
    extracted: Optional[ExtractedDataSchema] = None
    checked_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "check_id": "abc123e4-5678-90ab-cdef-ghijklmnopqr",
                "status": "rejected",
                "status_label": "Нельзя заявлять в банк",
                "reason": "Отсутствует спецификация к договору.",
                "issues": [
                    {"level": "error", "message": "Отсутствует обязательный документ: спецификация"},
                    {"level": "warning", "message": "Не удалось определить тип документа: «scan_0041.jpg»"}
                ],
                "documents": [
                    {"name": "договор_47.pdf", "detected_type": "contract", "size_kb": 142}
                ],
                "extracted": {
                    "contractor": "ООО «ТехАгро»",
                    "amount": "1 250 000 ₽",
                    "date": "01.03.2025",
                    "subject": "Поставка минеральных удобрений"
                },
                "checked_at": "2025-03-15T14:32:00Z"
            }
        }
    }


class CheckListItem(BaseModel):
    """Краткая информация о проверке для списка (GET /api/checks)."""
    id: uuid.UUID
    created_at: datetime
    program: ProgramType
    status: str
    documents_count: int

    model_config = {"from_attributes": True}


class ChecksListResponse(BaseModel):
    """Ответ со списком проверок."""
    checks: list[CheckListItem]
    total: int


# Схемы для валидации входящих данных (если понадобятся)
class CheckCreateRequest(BaseModel):
    """Запрос на создание проверки (для future использования)."""
    program: ProgramType