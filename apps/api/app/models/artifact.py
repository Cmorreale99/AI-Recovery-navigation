from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base, TimestampMixin, UUIDMixin


class GeneratedArtifact(UUIDMixin, TimestampMixin, Base):
    """A clinician-reviewable output artifact (gold layer).

    `content` holds the structured artifact body including source labels and
    per-claim confidence levels (Phase 6). `version` increments per regeneration
    so prior versions are retained rather than overwritten.
    """

    __tablename__ = "generated_artifacts"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # relapse_risk_map | urge_decoder | resource_plan | clinician_handoff | relapse_protocol
    artifact_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="generated")
    content: Mapped[dict] = mapped_column(JSONB, nullable=False)
