import pytest
from app.domain.documents.detector import detect_document_type, is_valid_extension
from app.common.enums import DocumentType
from app.domain.checks.constants import ALLOWED_EXTENSIONS


class TestDetectDocumentType:
    """Тесты определения типа документа по имени файла."""
    
    def test_detect_contract_russian(self):
        """Договор на русском."""
        assert detect_document_type("договор_поставки_2025.pdf") == DocumentType.CONTRACT
    
    def test_detect_contract_english(self):
        """Договор на английском."""
        assert detect_document_type("contract_001.docx") == DocumentType.CONTRACT
    
    def test_detect_invoice_with_numbers(self):
        """Счёт с номером и датой."""
        assert detect_document_type("Счёт №123 от 01.03.2025.pdf") == DocumentType.INVOICE
    
    def test_detect_invoice_without_yo(self):
        """Счёт без буквы ё."""
        assert detect_document_type("счет_456.docx") == DocumentType.INVOICE
    
    def test_detect_act_russian(self):
        """Акт на русском."""
        assert detect_document_type("Акт выполненных работ.pdf") == DocumentType.ACT
    
    def test_detect_upd(self):
        """УПД (универсальный передаточный документ)."""
        assert detect_document_type("УПД №789.pdf") == DocumentType.ACT
    
    def test_detect_specification(self):
        """Спецификация."""
        assert detect_document_type("спецификация_к_договору.pdf") == DocumentType.SPECIFICATION
    
    def test_detect_unknown_file(self):
        """Неизвестный тип файла."""
        assert detect_document_type("scan_0041.jpg") == DocumentType.UNKNOWN
    
    def test_detect_unknown_random_name(self):
        """Случайное имя без ключевых слов."""
        assert detect_document_type("document_final_v2.pdf") == DocumentType.UNKNOWN
    
    def test_case_insensitive(self):
        """Регистронезависимый поиск."""
        assert detect_document_type("ДОГОВОР.PDF") == DocumentType.CONTRACT
        assert detect_document_type("Invoice_123.docx") == DocumentType.INVOICE


class TestIsValidExtension:
    """Тесты проверки допустимых расширений."""
    
    def test_valid_pdf(self):
        assert is_valid_extension("file.pdf", ALLOWED_EXTENSIONS) is True
    
    def test_valid_docx(self):
        assert is_valid_extension("file.docx", ALLOWED_EXTENSIONS) is True
    
    def test_valid_jpg(self):
        assert is_valid_extension("file.jpg", ALLOWED_EXTENSIONS) is True
    
    def test_valid_png(self):
        assert is_valid_extension("file.png", ALLOWED_EXTENSIONS) is True
    
    def test_invalid_txt(self):
        assert is_valid_extension("file.txt", ALLOWED_EXTENSIONS) is False
    
    def test_invalid_exe(self):
        assert is_valid_extension("malware.exe", ALLOWED_EXTENSIONS) is False
    
    def test_no_extension(self):
        assert is_valid_extension("no_extension", ALLOWED_EXTENSIONS) is False