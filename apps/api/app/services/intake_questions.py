"""Canonical structured intake question catalog.

These are **structured intake questions** (symptom and support questions) — never
framed as diagnostic questions in the UI. The app asks about symptoms and support
needs but does not diagnose. `category` values align with the extraction entity
categories so downstream extraction (Phase 4+) can map answers to silver entities.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Question:
    key: str
    label: str
    category: str
    type: str  # text | textarea | single_select | multi_select | date
    group: str
    help: str | None = None
    options: tuple[str, ...] = field(default_factory=tuple)


INTAKE_QUESTIONS: tuple[Question, ...] = (
    # --- Your goal ---
    Question(
        key="goal",
        label="What is your current goal?",
        category="goal",
        type="single_select",
        group="Your goal",
        options=(
            "Quit",
            "Reduce",
            "Maintain sobriety",
            "Prevent relapse",
            "Unsure",
        ),
    ),
    Question(
        key="urgency",
        label="How urgent does your situation feel right now?",
        category="constraint",
        type="single_select",
        group="Your goal",
        options=("Low", "Moderate", "High", "Urgent"),
    ),
    # --- Substance use ---
    Question(
        key="primary_substances",
        label="Primary substance(s)",
        category="substance",
        type="text",
        group="Substance use",
        help="You can list more than one, separated by commas.",
    ),
    Question(
        key="use_pattern",
        label="Last use date or current use pattern",
        category="use_pattern",
        type="textarea",
        group="Substance use",
    ),
    Question(
        key="longest_sober",
        label="Previous longest sober period",
        category="use_pattern",
        type="text",
        group="Substance use",
    ),
    Question(
        key="prior_treatment",
        label="Prior treatment history",
        category="treatment_preference",
        type="textarea",
        group="Substance use",
        help="Optional. Past programs, therapy, medications, or supports you've tried.",
    ),
    # --- Symptom and support questions ---
    Question(
        key="withdrawal_symptoms",
        label="Withdrawal symptoms you've noticed",
        category="withdrawal_symptom",
        type="textarea",
        group="Symptom and support questions",
    ),
    Question(
        key="current_symptoms",
        label="Current symptoms",
        category="symptom",
        type="textarea",
        group="Symptom and support questions",
    ),
    Question(
        key="sleep_problems",
        label="Sleep problems",
        category="symptom",
        type="textarea",
        group="Symptom and support questions",
    ),
    Question(
        key="conditions_disclosed",
        label="Diagnoses or conditions you want to share (optional)",
        category="condition_mentioned",
        type="textarea",
        group="Symptom and support questions",
        help="This app does not diagnose. Share only what you choose to disclose.",
    ),
    Question(
        key="neuro_trauma_notes",
        label="Neuropsych / ADHD / autism / trauma notes (optional)",
        category="condition_mentioned",
        type="textarea",
        group="Symptom and support questions",
    ),
    Question(
        key="medications",
        label="Current medications you want to mention (optional)",
        category="medication_mentioned",
        type="textarea",
        group="Symptom and support questions",
        help="This app does not advise any changes to your medications.",
    ),
    Question(
        key="current_supports",
        label="Current supports (people, groups, sponsor, coach, etc.)",
        category="support",
        type="textarea",
        group="Symptom and support questions",
    ),
    # --- Access & preferences ---
    Question(
        key="insurance",
        label="Insurance",
        category="constraint",
        type="text",
        group="Access & preferences",
    ),
    Question(
        key="budget",
        label="Budget constraints",
        category="constraint",
        type="text",
        group="Access & preferences",
    ),
    Question(
        key="location",
        label="Location (city / region)",
        category="constraint",
        type="text",
        group="Access & preferences",
    ),
    Question(
        key="preferred_modalities",
        label="Preferred support modalities",
        category="treatment_preference",
        type="multi_select",
        group="Access & preferences",
        options=(
            "SMART Recovery",
            "AA / NA",
            "Therapy",
            "IOP / PHP",
            "Psychiatry",
            "Medication-assisted treatment discussion",
            "Recovery coaching",
            "Peer support",
            "Sober living",
            "Other",
        ),
    ),
)

_BY_KEY = {q.key: q for q in INTAKE_QUESTIONS}


def get_question(key: str) -> Question | None:
    return _BY_KEY.get(key)


def questions_as_dicts() -> list[dict]:
    return [
        {
            "key": q.key,
            "label": q.label,
            "category": q.category,
            "type": q.type,
            "group": q.group,
            "help": q.help,
            "options": list(q.options),
        }
        for q in INTAKE_QUESTIONS
    ]
