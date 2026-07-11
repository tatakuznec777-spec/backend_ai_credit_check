import uuid
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.checks.models import Check, Document


async def create_check(
    session: AsyncSession,
    program: str,
    status: str,
    reason: str | None = None,
    extracted_data: dict | None = None,
    documents: list[dict] | None = None,
) -> Check:
    """Создать новую проверку с документами"""
    check = Check(
        program=program,
        status=status,
        reason=reason,
        extracted_data=extracted_data,
    )
    
    if documents:
        for doc_data in documents:
            doc = Document(
                check_id=check.id,
                file_name=doc_data["file_name"],
                detected_type=doc_data.get("detected_type"),
                size_kb=doc_data.get("size_kb", 0),
                issues=doc_data.get("issues"),
            )
            check.documents.append(doc)
    
    session.add(check)
    await session.flush()
    return check


async def get_check_by_id(session: AsyncSession, check_id: uuid.UUID) -> Check | None:
    """Получить проверку по ID с документами"""
    result = await session.execute(
        select(Check)
        .options(selectinload(Check.documents))
        .where(Check.id == check_id)
    )
    return result.scalar_one_or_none()


async def list_checks(
    session: AsyncSession,
    limit: int = 100,
    offset: int = 0,
) -> list[Check]:
    """Получить список всех проверок с документами (eager loading)"""
    result = await session.execute(
        select(Check)
        .options(selectinload(Check.documents))  # ← ДОБАВЛЕНО: явная загрузка документов
        .order_by(desc(Check.created_at))
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all())