from pathlib import Path
from app.common.enums import DocumentType
from app.domain.documents.patterns import get_pattern_for_type


# Порядок проверки типов документов (от более специфичных к более общим)
DETECTION_ORDER = [
    DocumentType.SPECIFICATION,
    DocumentType.INVOICE,
    DocumentType.CONTRACT,
    DocumentType.ACT,
]


def detect_document_type(filename: str) -> DocumentType:
    """
    Определить тип документа по имени файла.
    
    Args:
        filename: Имя файла (например, "договор_поставки_2025.pdf")
    
    Returns:
        DocumentType: Определённый тип документа или UNKNOWN
    """
    # Извлекаем имя без пути и расширения
    name = Path(filename).stem.lower()
    
    # Заменяем _ на пробел для корректной работы границ слов (\b)
    name_normalized = name.replace('_', ' ')
    
    # Проходим по типам документов в определённом порядке
    for doc_type in DETECTION_ORDER:
        pattern = get_pattern_for_type(doc_type)
        if pattern.search(name_normalized):
            return doc_type
    
    return DocumentType.UNKNOWN


def is_valid_extension(filename: str, allowed_extensions: set[str]) -> bool:
    """
    Проверить, что расширение файла допустимо.
    
    Args:
        filename: Имя файла
        allowed_extensions: Набор допустимых расширений (например, {'.pdf', '.docx'})
    
    Returns:
        bool: True, если расширение допустимо
    """
    ext = Path(filename).suffix.lower()
    return ext in allowed_extensions