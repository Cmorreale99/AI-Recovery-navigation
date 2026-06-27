from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConsentIn(BaseModel):
    consent_type: str = "data_processing"
    version: str = "v1"
    granted: bool


class ConsentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    consent_type: str
    version: str
    granted: bool
    created_at: datetime
