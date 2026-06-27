from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


# --- Question catalog (served to the frontend so it can render the form) ---
class QuestionOut(BaseModel):
    key: str
    label: str
    category: str
    type: str  # text | textarea | single_select | multi_select | date
    group: str
    help: str | None = None
    options: list[str] = []


class IntakeQuestionsOut(BaseModel):
    questions: list[QuestionOut]


# --- Sessions & answers ---
class IntakeStartOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: str
    created_at: datetime


class IntakeAnswerIn(BaseModel):
    question_key: str
    value: Any = None


class IntakeAnswersIn(BaseModel):
    session_id: uuid.UUID
    answers: list[IntakeAnswerIn]
    complete: bool = False


class IntakeAnswerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    question_key: str
    question_label: str | None
    category: str | None
    value: Any
    created_at: datetime


class IntakeSessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: str
    created_at: datetime
    completed_at: datetime | None


class IntakeLatestOut(BaseModel):
    session: IntakeSessionOut | None
    answers: list[IntakeAnswerOut]
