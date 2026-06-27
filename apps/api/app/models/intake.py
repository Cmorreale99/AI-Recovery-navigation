from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base, TimestampMixin, UUIDMixin


class IntakeSession(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "intake_sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # "started" | "completed"
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="started")
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class IntakeAnswer(UUIDMixin, TimestampMixin, Base):
    """One structured intake answer.

    Stored generically (key + JSONB value) so the question set can evolve without
    a schema migration. These are structured intake questions, never framed as
    diagnostic questions in the UI.
    """

    __tablename__ = "intake_answers"

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("intake_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question_key: Mapped[str] = mapped_column(String(100), nullable=False)
    question_label: Mapped[str | None] = mapped_column(String(300), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Flexible value: string, list, number, etc.
    value: Mapped[dict | list | str | None] = mapped_column(JSONB, nullable=True)
