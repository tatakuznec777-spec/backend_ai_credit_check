"""
Модуль для извлечения данных из документов.

TODO: В рамках MVP реализована заглушка.
Для production-версии необходимо интегрировать:
- pdfplumber для PDF
- python-docx для DOCX
- Tesseract OCR для изображений (JPG/PNG), если потребуется
- NLP/regex для извлечения контрагента, суммы, даты, предмета
"""
from app.common.enums import DocumentType


def extract_document_data(file_bytes: bytes, doc_type: DocumentType) -> dict:
    """
    Извлечь данные из документа.
    
    Args:
        file_bytes: Содержимое файла в байтах
        doc_type: Тип документа
    
    Returns:
        dict: Извлечённые данные (contractor, amount, date, subject)
    """
    # TODO: Реализовать реальный парсинг
    # Пока возвращаем заглушку для демонстрации структуры ответа
    return {
        "contractor": "ООО «ТехАгро»",
        "amount": "1 250 000 ₽",
        "date": "01.03.2025",
        "subject": "Поставка минеральных удобрений",
    }