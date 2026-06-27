"""Shared FastAPI dependencies."""

from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User
from app.services.users import get_or_create_demo_user


def get_current_user(db: Session = Depends(get_db)) -> User:
    """v1: resolve to the seeded demo user (no auth). See services.users."""
    return get_or_create_demo_user(db)
