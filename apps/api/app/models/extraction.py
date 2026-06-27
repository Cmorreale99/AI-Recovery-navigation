from __future__ import annotations

import uuid

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base, TimestampMixin, UUIDMixin


class ExtractedEntity(UUIDMixin, TimestampMixin, Base):
    """A structured recovery-relevant entity (silver layer).

    Follows the README extraction contract: every entity carries label, category,
    source_text, source_type, source_id, confidence, and extraction_method.
    `source_id` is an untyped reference to the originating row (intake answer,
    journal entry, or document chunk) identified together with `source_type`.
    """

    __tablename__ = "extracted_entities"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    label: Mapped[str] = mapped_column(String(300), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    source_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    # intake | journal | document | tracker | inference
    source_type: Mapped[str] = mapped_column(String(20), nullable=False)
    source_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    # e.g. "heuristic", "mock_llm", "llm"
    extraction_method: Mapped[str | None] = mapped_column(String(50), nullable=True)
