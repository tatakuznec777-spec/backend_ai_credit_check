from enum import StrEnum

class ProgramType(StrEnum):
    """Тип программы проверки."""
    FEDERAL = "federal"
    REGIONAL = "regional"

class CheckStatus(StrEnum):
    """Итоговый статус проверки."""
    IN_PROGRESS = "check_in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"

class IssueLevel(StrEnum):
    """Уровень проблемы."""
    ERROR = "error"
    WARNING = "warning"

class DocumentType(StrEnum):
    """Тип документа."""
    CONTRACT = "contract"           # Договор
    SPECIFICATION = "specification" # Спецификация
    INVOICE = "invoice"             # Счёт
    ACT = "act"                     # Акт / УПД
    UNKNOWN = "unknown"             # Не удалось определить