from app.common.enums import DocumentType, ProgramType

# Обязательные наборы документов по программам
REQUIRED_DOCUMENTS: dict[ProgramType, set[DocumentType]] = {
    ProgramType.FEDERAL: {
        DocumentType.CONTRACT,
        DocumentType.SPECIFICATION,
        DocumentType.INVOICE,
        DocumentType.ACT,
    },
    ProgramType.REGIONAL: {
        DocumentType.CONTRACT,
        DocumentType.INVOICE,
        DocumentType.ACT,
    },
}

# Допустимые расширения файлов
ALLOWED_EXTENSIONS: set[str] = {".pdf", ".docx", ".jpg", ".jpeg", ".png"}

# Допустимые MIME-типы (для проверки magic bytes)
ALLOWED_MIME_TYPES: set[str] = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "image/jpeg",
    "image/png",
}

# Максимальный размер файла в байтах (20 МБ)
MAX_FILE_SIZE_BYTES: int = 20 * 1024 * 1024