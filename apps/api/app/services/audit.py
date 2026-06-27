"""Audit logging helper.

Privacy: `context` must contain non-sensitive metadata only (ids, counts,
outcome flags) — never raw intake/journal/document text. Caller is responsible
for committing the surrounding transaction; this only stages the row.
"""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.models import AuditLog


def record_audit(
    db: Session,
    *,
    user_id: uuid.UUID | None,
    action: str,
    entity_type: str | None = None,
    entity_id: uuid.UUID | None = None,
    context: dict | None = None,
) -> None:
    db.add(
        AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            context=context,
        )
    )
