import uuid
from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from app.common.enums import CheckStatus, DocumentType, IssueLevel, ProgramType
from app.domain.checks.constants import REQUIRED_DOCUMENTS, ALLOWED_EXTENSIONS
from app.domain.checks.models import Check, Document
from app.domain.checks.repository import create_check, get_check_by_id, list_checks
from app.domain.checks.schemas import (
    CheckResponse,
    CheckListItem,
    ChecksListResponse,
    DocumentSchema,
    ExtractedDataSchema,
    IssueSchema,
)
from app.domain.documents.detector import detect_document_type, is_valid_extension
from app.domain.documents.parser import extract_document_data
from app.domain.checks.service import (
    determine_final_status,
    check_document_completeness,
    create_unknown_document_warning,
)
from app.infrastructure.database import get_db_session
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


def get_status_label(status: str) -> str:
    """Возвращает человекочитаемый статус."""
    labels = {
        "approved": "Все документы в порядке",
        "rejected": "Нельзя заявлять в банк",
        "check_in_progress": "Проверка выполняется",
    }
    return labels.get(status, status)


@router.get("", response_model=ChecksListResponse, summary="Список всех проверок")
async def get_checks(
    session: AsyncSession = Depends(get_db_session),
):
    """Получить список всех проверок."""
    try:
        # Используем repository функцию с eager loading
        checks = await list_checks(session)
        
        items = []
        for check in checks:
            items.append(CheckListItem(
                id=check.id,
                created_at=check.created_at,
                program=check.program,
                status=check.status,
                documents_count=len(check.documents),
            ))
        
        return ChecksListResponse(checks=items, total=len(items))
    except Exception as e:
        print(f"ERROR in get_checks: {e}")
        import traceback
        traceback.print_exc()
        raise


@router.get("/{check_id}", response_model=CheckResponse, summary="Детали проверки")
async def get_check(
    check_id: uuid.UUID,
    session: AsyncSession = Depends(get_db_session),
):
    """Получить полную информацию о проверке по ID."""
    check = await get_check_by_id(session, check_id)
    if not check:
        raise HTTPException(status_code=404, detail="Проверка не найдена")
    
    return CheckResponse(
        check_id=check.id,
        status=check.status,
        status_label=get_status_label(check.status),
        reason=check.reason,
        issues=[],
        documents=[DocumentSchema(
            name=doc.file_name,
            detected_type=doc.detected_type,
            size_kb=doc.size_kb,
        ) for doc in check.documents],
        extracted=ExtractedDataSchema(**check.extracted_data) if check.extracted_data else None,
        checked_at=check.created_at,
    )


@router.post("", response_model=CheckResponse, summary="Загрузить документы на проверку")
async def create_check_endpoint(
    program: str = Form(..., description="Тип программы (federal или regional)"),
    files: List[UploadFile] = File(..., description="Файлы документов"),
    session: AsyncSession = Depends(get_db_session),
):
    """Загрузить пакет документов для проверки."""
    try:
        # Валидация program
        try:
            program_enum = ProgramType(program)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Неверный тип программы: {program}")
        
        # Валидация количества файлов
        if len(files) > settings.max_files_per_request:
            raise HTTPException(
                status_code=400,
                detail=f"Слишком много файлов. Максимум: {settings.max_files_per_request}"
            )
        
        issues = []
        documents_data = []
        detected_types = set()
        
        # Обрабатываем каждый файл
        for file in files:
            # Проверка расширения
            if not is_valid_extension(file.filename, ALLOWED_EXTENSIONS):
                issues.append(IssueSchema(
                    level=IssueLevel.ERROR,
                    message=f"Недопустимый формат файла: {file.filename}"
                ))
                continue
            
            # Проверка размера
            contents = await file.read()
            file_size = len(contents)
            if file_size > settings.max_file_size_bytes:
                issues.append(IssueSchema(
                    level=IssueLevel.ERROR,
                    message=f"Файл {file.filename} превышает максимальный размер 20 МБ"
                ))
                continue
            
            # Определение типа документа
            doc_type = detect_document_type(file.filename)
            if doc_type == DocumentType.UNKNOWN:
                issues.append(create_unknown_document_warning(file.filename))
            else:
                detected_types.add(doc_type)
            
            # Сохраняем информацию о документе
            documents_data.append({
                "file_name": file.filename,
                "detected_type": doc_type.value if doc_type != DocumentType.UNKNOWN else None,
                "size_kb": file_size // 1024,
                "issues": [],
            })
        
        # Проверка комплектности
        completeness_issues = check_document_completeness(detected_types, program_enum)
        for issue in completeness_issues:
            issues.append(IssueSchema(**issue))
        
        # Определение финального статуса
        final_status = determine_final_status([i.model_dump() for i in issues])
        
        # Формируем reason
        reason = None
        if final_status == CheckStatus.REJECTED:
            error_messages = [i.message for i in issues if i.level == IssueLevel.ERROR]
            reason = ". ".join(error_messages) if error_messages else "Неизвестная ошибка"
        
        # Извлечение данных (заглушка)
        extracted_data = None
        if final_status == CheckStatus.APPROVED:
            extracted_data = {
                "contractor": "ООО «ТехАгро»",
                "amount": "1 250 000 ₽",
                "date": "01.03.2025",
                "subject": "Поставка минеральных удобрений",
            }
        
        # Создаём запись в БД
        check = await create_check(
            session=session,
            program=program_enum.value,
            status=final_status.value,
            reason=reason,
            extracted_data=extracted_data,
            documents=documents_data,
        )
        
        # Формируем ответ
        response = CheckResponse(
            check_id=check.id,
            status=check.status,
            status_label=get_status_label(check.status),
            reason=reason,
            issues=issues,
            documents=[DocumentSchema(
                name=doc["file_name"],
                detected_type=doc["detected_type"],
                size_kb=doc["size_kb"],
            ) for doc in documents_data],
            extracted=ExtractedDataSchema(**extracted_data) if extracted_data else None,
            checked_at=datetime.now(timezone.utc),
        )
        
        return response
    except Exception as e:
        print(f"ERROR in create_check_endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise