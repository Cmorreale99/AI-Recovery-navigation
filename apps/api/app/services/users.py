"""User resolution.

v1 has no authentication. A single seeded demo user stands in for the current
user so the local flow works end-to-end. Real auth is out of scope for the MVP.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User

DEMO_EMAIL = "demo@local"


def get_or_create_demo_user(db: Session) -> User:
    user = db.execute(
        select(User).where(User.email == DEMO_EMAIL)
    ).scalar_one_or_none()
    if user is None:
        user = User(email=DEMO_EMAIL, display_name="Demo User", is_demo=True)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
