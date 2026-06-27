"""SQLAlchemy ORM models.

Organized along the README's medallion layers:
- operational: User, Consent, IntakeSession, IntakeAnswer, JournalEntry, AuditLog
- bronze/raw -> silver: Document, DocumentChunk, ExtractedEntity
- gold: GeneratedArtifact
- safety: SafetyEvent
"""

from app.models.artifact import GeneratedArtifact
from app.models.audit import AuditLog
from app.models.consent import Consent
from app.models.document import Document, DocumentChunk
from app.models.extraction import ExtractedEntity
from app.models.intake import IntakeAnswer, IntakeSession
from app.models.journal import JournalEntry
from app.models.safety import SafetyEvent
from app.models.user import User

__all__ = [
    "User",
    "Consent",
    "IntakeSession",
    "IntakeAnswer",
    "JournalEntry",
    "Document",
    "DocumentChunk",
    "ExtractedEntity",
    "GeneratedArtifact",
    "SafetyEvent",
    "AuditLog",
]
