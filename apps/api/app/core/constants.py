"""Controlled vocabularies shared across models and services.

Stored as plain strings (not Postgres ENUM types) to keep migrations simple and
local-first. Treat these tuples as the allowed values; validation lives in the
service/schema layer added in later phases.
"""

from __future__ import annotations

# Where an extracted entity / safety event originated.
SOURCE_TYPES = ("intake", "journal", "document", "tracker", "inference")

# Gold-layer artifact kinds (one generator per type, Phase 6).
ARTIFACT_TYPES = (
    "relapse_risk_map",
    "urge_decoder",
    "resource_plan",
    "clinician_handoff",
    "relapse_protocol",
)

# Deterministic safety classifier categories (Phase 5).
SAFETY_CATEGORIES = (
    "suicidality",
    "overdose",
    "dangerous_intoxication",
    "dangerous_withdrawal",
    "psychosis_mania",
    "medication_misuse",
    "imminent_relapse",
    "impaired_driving",
    "medical_danger",
)

SAFETY_SEVERITIES = ("low", "moderate", "high", "severe")

# Extraction entity categories (silver layer), per README extraction rules.
ENTITY_CATEGORIES = (
    "substance",
    "use_pattern",
    "withdrawal_symptom",
    "symptom",
    "condition_mentioned",
    "medication_mentioned",
    "trigger",
    "high_risk_state",
    "urge_phrase",
    "protective_factor",
    "coping_action",
    "constraint",
    "support",
    "treatment_preference",
    "safety_flag",
)
