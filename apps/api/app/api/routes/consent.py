from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import Consent, User
from app.schemas.consent import ConsentIn, ConsentOut
from app.services.audit import record_audit

router = APIRouter(tags=["user"])


@router.post("/consent", response_model=ConsentOut)
def post_consent(
    payload: ConsentIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Consent:
    consent = Consent(
        user_id=user.id,
        consent_type=payload.consent_type,
        version=payload.version,
        granted=payload.granted,
    )
    db.add(consent)
    record_audit(
        db,
        user_id=user.id,
        action="consent_recorded",
        entity_type="consent",
        context={
            "consent_type": payload.consent_type,
            "version": payload.version,
            "granted": payload.granted,
        },
    )
    db.commit()
    db.refresh(consent)
    return consent
