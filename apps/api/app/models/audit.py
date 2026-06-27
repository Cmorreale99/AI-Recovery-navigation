from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base, TimestampMixin, UUIDMixin


class AuditLog(UUIDMixin, TimestampMixin, Base):
    """Internal audit trail for sensitive actions.

    Privacy: `context` holds non-sensitive metadata only (ids, counts, action
    outcome) — never raw intake/journal/document text. The attribute is named
    `context` because `metadata` is reserved by SQLAlchemy's declarative base.
    """

    __tablename__ = "audit_logs"

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    # e.g. intake_submitted, journal_created, document_uploaded, extraction_run,
    # artifact_generated, safety_classified, export_generated
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    entity_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    context: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
