import pytest
from app.domain.checks.service import (
    determine_final_status,
    check_document_completeness,
    create_unknown_document_warning,
)
from app.common.enums import CheckStatus, DocumentType, IssueLevel, ProgramType


class TestDetermineFinalStatus:
    """Тесты определения итогового статуса."""
    
    def test_approved_when_no_issues(self):
        """Нет проблем -> approved."""
        assert determine_final_status([]) == CheckStatus.APPROVED
    
    def test_approved_when_only_warnings(self):
        """Только warnings -> approved."""
        issues = [
            {"level": IssueLevel.WARNING, "message": "test warning"},
        ]
        assert determine_final_status(issues) == CheckStatus.APPROVED
    
    def test_rejected_when_has_error(self):
        """Хотя бы одна ошибка -> rejected."""
        issues = [
            {"level": IssueLevel.WARNING, "message": "warning"},
            {"level": IssueLevel.ERROR, "message": "error"},
        ]
        assert determine_final_status(issues) == CheckStatus.REJECTED
    
    def test_rejected_when_multiple_errors(self):
        """Несколько ошибок -> rejected."""
        issues = [
            {"level": IssueLevel.ERROR, "message": "error 1"},
            {"level": IssueLevel.ERROR, "message": "error 2"},
        ]
        assert determine_final_status(issues) == CheckStatus.REJECTED


class TestCheckDocumentCompleteness:
    """Тесты проверки комплектности документов."""
    
    def test_federal_complete(self):
        """Federal: все документы есть."""
        detected = {
            DocumentType.CONTRACT,
            DocumentType.SPECIFICATION,
            DocumentType.INVOICE,
            DocumentType.ACT,
        }
        issues = check_document_completeness(detected, ProgramType.FEDERAL)
        assert len(issues) == 0
    
    def test_federal_missing_specification(self):
        """Federal: не хватает спецификации."""
        detected = {
            DocumentType.CONTRACT,
            DocumentType.INVOICE,
            DocumentType.ACT,
        }
        issues = check_document_completeness(detected, ProgramType.FEDERAL)
        assert len(issues) == 1
        assert "specification" in issues[0]["message"]
    
    def test_regional_complete(self):
        """Regional: все документы есть."""
        detected = {
            DocumentType.CONTRACT,
            DocumentType.INVOICE,
            DocumentType.ACT,
        }
        issues = check_document_completeness(detected, ProgramType.REGIONAL)
        assert len(issues) == 0
    
    def test_regional_missing_act(self):
        """Regional: не хватает акта."""
        detected = {
            DocumentType.CONTRACT,
            DocumentType.INVOICE,
        }
        issues = check_document_completeness(detected, ProgramType.REGIONAL)
        assert len(issues) == 1
        assert "act" in issues[0]["message"]


class TestCreateUnknownDocumentWarning:
    """Тесты создания warning для нераспознанных файлов."""
    
    def test_warning_message_format(self):
        """Проверка формата сообщения."""
        warning = create_unknown_document_warning("scan_0041.jpg")
        assert warning["level"] == IssueLevel.WARNING
        assert "scan_0041.jpg" in warning["message"]