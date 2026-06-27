"""Integration tests for the consent + structured intake flow.

Skipped automatically when no database is available (see conftest `db`).
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_me_returns_demo_user(db) -> None:
    resp = client.get("/me")
    assert resp.status_code == 200
    assert resp.json()["is_demo"] is True


def test_consent_recorded(db) -> None:
    resp = client.post("/consent", json={"granted": True})
    assert resp.status_code == 200
    body = resp.json()
    assert body["granted"] is True
    assert body["consent_type"] == "data_processing"


def test_full_intake_flow(db) -> None:
    questions = client.get("/intake/questions").json()["questions"]
    assert any(q["key"] == "goal" for q in questions)

    session = client.post("/intake/start").json()
    assert session["status"] == "started"

    resp = client.post(
        "/intake/answers",
        json={
            "session_id": session["id"],
            "answers": [
                {"question_key": "goal", "value": "Quit"},
                {"question_key": "preferred_modalities", "value": ["Therapy", "SMART Recovery"]},
            ],
            "complete": True,
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["session"]["status"] == "completed"
    # Server enriches answers with catalog label/category.
    goal = next(a for a in body["answers"] if a["question_key"] == "goal")
    assert goal["category"] == "goal"
    assert goal["question_label"]

    latest = client.get("/intake/latest").json()
    assert latest["session"] is not None


def test_answers_unknown_session_404(db) -> None:
    resp = client.post(
        "/intake/answers",
        json={
            "session_id": "00000000-0000-0000-0000-000000000000",
            "answers": [],
            "complete": False,
        },
    )
    assert resp.status_code == 404
