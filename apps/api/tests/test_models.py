"""Validates the ORM metadata registers all 11 Phase 2 tables.

Runs without a database connection — it only inspects mapper metadata.
"""

from app.db.base import Base

EXPECTED_TABLES = {
    "users",
    "consents",
    "intake_sessions",
    "intake_answers",
    "journal_entries",
    "documents",
    "document_chunks",
    "extracted_entities",
    "generated_artifacts",
    "safety_events",
    "audit_logs",
}


def test_all_tables_registered() -> None:
    assert EXPECTED_TABLES.issubset(set(Base.metadata.tables))


def test_every_table_has_pk_and_created_at() -> None:
    for name in EXPECTED_TABLES:
        table = Base.metadata.tables[name]
        assert table.primary_key.columns.keys() == ["id"]
        assert "created_at" in table.columns
