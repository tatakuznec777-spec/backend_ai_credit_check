import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database import Base


class Check(Base):
    """Модель проверки пакета документов."""
    
    __tablename__ = "checks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    program: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="check_in_progress")
    reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    extracted_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # Связь с документами
    documents: Mapped[list["Document"]] = relationship(
        back_populates="check",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Check(id={self.id}, program={self.program}, status={self.status})>"


class Document(Base):
    """Модель документа в проверке."""
    
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    check_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("checks.id", ondelete="CASCADE"),  # ← ДОБАВЛЕНО ForeignKey
        nullable=False,
    )
    file_name: Mapped[str] = mapped_column(String(500), nullable=False)
    detected_type: Mapped[str | None] = mapped_column(String(30), nullable=True)
    size_kb: Mapped[int] = mapped_column(nullable=False, default=0)
    issues: Mapped[list | None] = mapped_column(JSONB, nullable=True)

    # Связь с проверкой
    check: Mapped["Check"] = relationship(back_populates="documents")

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, file_name={self.file_name}, type={self.detected_type})>"