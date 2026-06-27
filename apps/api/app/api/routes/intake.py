from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import IntakeAnswer, IntakeSession, User
from app.schemas.intake import (
    IntakeAnswersIn,
    IntakeLatestOut,
    IntakeQuestionsOut,
    IntakeStartOut,
)
from app.services.audit import record_audit
from app.services.intake_questions import get_question, questions_as_dicts

router = APIRouter(prefix="/intake", tags=["intake"])


def _latest_payload(db: Session, user: User) -> IntakeLatestOut:
    session = db.execute(
        select(IntakeSession)
        .where(IntakeSession.user_id == user.id)
        .order_by(IntakeSession.created_at.desc())
        .limit(1)
    ).scalar_one_or_none()

    if session is None:
        return IntakeLatestOut(session=None, answers=[])

    answers = db.execute(
        select(IntakeAnswer)
        .where(IntakeAnswer.session_id == session.id)
        .order_by(IntakeAnswer.created_at.asc())
    ).scalars().all()

    return IntakeLatestOut.model_validate(
        {"session": session, "answers": answers}, from_attributes=True
    )


@router.get("/questions", response_model=IntakeQuestionsOut)
def get_questions() -> dict:
    return {"questions": questions_as_dicts()}


@router.post("/start", response_model=IntakeStartOut)
def start_intake(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> IntakeSession:
    session = IntakeSession(user_id=user.id, status="started")
    db.add(session)
    db.flush()
    record_audit(
        db,
        user_id=user.id,
        action="intake_started",
        entity_type="intake_session",
        entity_id=session.id,
    )
    db.commit()
    db.refresh(session)
    return session


@router.post("/answers", response_model=IntakeLatestOut)
def submit_answers(
    payload: IntakeAnswersIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> IntakeLatestOut:
    session = db.get(IntakeSession, payload.session_id)
    if session is None or session.user_id != user.id:
        raise HTTPException(status_code=404, detail="Intake session not found")

    for answer in payload.answers:
        question = get_question(answer.question_key)
        db.add(
            IntakeAnswer(
                session_id=session.id,
                question_key=answer.question_key,
                question_label=question.label if question else None,
                category=question.category if question else None,
                value=answer.value,
            )
        )

    if payload.complete:
        session.status = "completed"
        session.completed_at = datetime.now(timezone.utc)

    record_audit(
        db,
        user_id=user.id,
        action="intake_answers_saved",
        entity_type="intake_session",
        entity_id=session.id,
        context={"answer_count": len(payload.answers), "complete": payload.complete},
    )
    db.commit()
    return _latest_payload(db, user)


@router.get("/latest", response_model=IntakeLatestOut)
def latest_intake(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> IntakeLatestOut:
    return _latest_payload(db, user)
