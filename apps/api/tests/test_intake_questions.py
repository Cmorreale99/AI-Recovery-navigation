"""Validates the structured intake question catalog (no DB required)."""

from app.services.intake_questions import (
    INTAKE_QUESTIONS,
    get_question,
    questions_as_dicts,
)


def test_keys_are_unique() -> None:
    keys = [q.key for q in INTAKE_QUESTIONS]
    assert len(keys) == len(set(keys))


def test_select_questions_have_options() -> None:
    for q in INTAKE_QUESTIONS:
        if q.type in ("single_select", "multi_select"):
            assert q.options, f"{q.key} is a select but has no options"
        else:
            assert not q.options


def test_required_intake_topics_present() -> None:
    keys = {q.key for q in INTAKE_QUESTIONS}
    required = {
        "goal",
        "primary_substances",
        "use_pattern",
        "withdrawal_symptoms",
        "current_symptoms",
        "conditions_disclosed",
        "medications",
        "insurance",
        "budget",
        "location",
        "preferred_modalities",
    }
    assert required.issubset(keys)


def test_get_question_and_dict_shape() -> None:
    assert get_question("goal") is not None
    assert get_question("does_not_exist") is None
    d = questions_as_dicts()[0]
    assert set(d) == {"key", "label", "category", "type", "group", "help", "options"}
