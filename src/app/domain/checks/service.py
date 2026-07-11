from app.common.enums import CheckStatus, DocumentType, IssueLevel, ProgramType
from app.domain.checks.constants import REQUIRED_DOCUMENTS
from app.domain.checks.schemas import IssueSchema


def determine_final_status(issues: list[dict]) -> CheckStatus:
    """
    Определить итоговый статус проверки на основе списка проблем
    
    Args:
        issues: Список проблем вида [{"level": "error", "message": "..."}, ...]
    
    Returns:
        CheckStatus: APPROVED если нет ошибок, REJECTED если есть хотя бы одна ошибка
    """
    has_errors = any(issue.get("level") == IssueLevel.ERROR for issue in issues)
    
    if has_errors:
        return CheckStatus.REJECTED
    
    return CheckStatus.APPROVED


def check_document_completeness(
    detected_types: set[DocumentType],
    program: ProgramType,
) -> list[dict]:
    """
    Проверить комплектность пакета документов
    
    Args:
        detected_types: Набор обнаруженных типов документов
        program: Тип программы (federal/regional)
    
    Returns:
        list[dict]: Список проблем (issues) уровня error для недостающих документов
    """
    required = REQUIRED_DOCUMENTS.get(program, set())
    missing = required - detected_types
    
    issues = []
    for doc_type in sorted(missing):
        issues.append({
            "level": IssueLevel.ERROR,
            "message": f"Отсутствует обязательный документ: {doc_type.value}",
        })
    
    return issues


def create_unknown_document_warning(filename: str) -> IssueSchema:
    """
    Создать warning для нераспознанного имени файла
    
    Args:
        filename: Имя файла
    
    Returns:
        IssueSchema: Проблема уровня warning
    """
    return IssueSchema(
        level=IssueLevel.WARNING,
        message=f"Не удалось определить тип документа: «{filename}»",
    )