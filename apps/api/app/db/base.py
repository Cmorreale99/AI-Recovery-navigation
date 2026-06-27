"""Imports Base metadata + all models.

Alembic targets `Base.metadata`; importing the models here ensures every table
is registered before autogenerate/migrations run.
"""

from app.db.base_class import Base  # noqa: F401
from app.models import (  # noqa: F401
    AuditLog,
    Consent,
    Document,
    DocumentChunk,
    ExtractedEntity,
    GeneratedArtifact,
    IntakeAnswer,
    IntakeSession,
    JournalEntry,
    SafetyEvent,
    User,
)
