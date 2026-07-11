import re
from app.common.enums import DocumentType

# Паттерны для определения типа документа по имени файла
# Используем \b для границ слов (работает после замены _ на пробел)
# Используем re.IGNORECASE для регистронезависимого поиска
DOCUMENT_PATTERNS: dict[DocumentType, list[str]] = {
    DocumentType.CONTRACT: [
        r"\bдоговор\b",
        r"\bcontract\b",
        r"\bdogovor\b",
        r"\bсоглашение\b",
        r"\bagreement\b",
    ],
    DocumentType.SPECIFICATION: [
        r"\bспецификац",  # спецификация, спецификации (без \b в конце, т.к. может быть окончание)
        r"\bspecification\b",
        r"\bspec\b",
        r"\bspetsifikatsiya\b",
    ],
    DocumentType.INVOICE: [
        r"\bсчёт\b",
        r"\bсчет\b",       # без ё
        r"\binvoice\b",
        r"\bschet\b",
    ],
    DocumentType.ACT: [
        r"\bакт\b",
        r"\bact\b",
        r"\bупд\b",
        r"\bupd\b",
        r"\bуниверсальный передаточный документ\b",
    ],
}


def get_pattern_for_type(doc_type: DocumentType) -> re.Pattern:
    """
    Скомпилировать regex-паттерн для типа документа
    Объединяет все паттерны через | (OR)
    """
    patterns = DOCUMENT_PATTERNS.get(doc_type, [])
    combined = "|".join(patterns)
    return re.compile(combined, re.IGNORECASE)