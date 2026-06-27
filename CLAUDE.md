# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Current state

This repository is **pre-implementation**: it contains only `README.md` (the full product/implementation spec), `LICENSE`, and a Python `.gitignore`. No application code, `docker-compose.yml`, or package manifests exist yet. The README is the source of truth — read it in full before building anything. Work proceeds through the 7 implementation phases defined at the bottom of the README (scaffold → schema → journal/docs → extraction/safety → artifacts → frontend → tests/docs).

## Non-negotiable product boundaries

This is a relapse-prevention / care-navigation planner for substance-use recovery. These constraints are the point of the product, not stylistic preferences — every feature, prompt, and output must honor them:

- **Never diagnose, prescribe, recommend medication changes, determine level of care autonomously, or replace clinical/medical care.** Outputs are *clinician-reviewable decision-support artifacts*, framed with hedged language ("Based on user-provided information…", "This may suggest…", "This is not medical advice.").
- **Never provide** substance procurement advice, dosing advice, detox/withdrawal instructions, or any encouragement to use — in code, prompts, or mock outputs.
- **The product is structured workflows + report generation, not a chatbot.** Do not build an unconstrained conversational agent as the main surface.
- **Safety classifier runs before any artifact generation.** It is deterministic and rule-based (keyword/phrase matching, see README "Safety classifier" section). On a high-risk hit, create a `safety_event`, return category + severity, route the frontend to the safety-escalation screen, and pause normal generation until acknowledged.
- **Do not fabricate real-world providers or clinical evidence.** When concrete resources are unavailable, generate a "search/action plan" instead of fake listings. For v1, resource data is local/mock; no web scraping.
- **Privacy:** consent row required before any processing; audit-log the sensitive actions (intake submit, journal create, doc upload, extraction, artifact gen, safety classify, export); never write raw sensitive user text to logs. This is explicitly **not production-compliant** — no real patient data.

## Intended architecture

Monorepo, local-first, runs via Docker Compose. Do not overbuild cloud infra.

- **Frontend:** Next.js + TypeScript + Tailwind. 12 pages (landing, consent, intake, journal, document upload, dashboard, relapse-risk map, urge decoder, resource plan, clinician handoff, relapse-prevention protocol, safety escalation).
- **Backend:** FastAPI + Python. SQLAlchemy + Alembic for ORM/migrations.
- **DB:** Postgres + pgvector. **Jobs:** Celery or RQ + Redis. **Storage:** filesystem abstraction in dev, S3-compatible interface later.
- **LLM + embeddings:** a single **provider-agnostic wrapper with mock mode as the default**. If no API key is present, produce deterministic mock outputs via heuristic extraction — the whole app must run end-to-end with no LLM key.

### Data model: medallion layers

Tables are organized as Bronze (raw: `raw_intake_responses`, `raw_journal_entries`, `raw_documents`, `upload_events`) → Silver (structured `extracted_*` entities + `document_chunks`/`document_embeddings`) → Gold (output artifacts: `relapse_risk_maps`, `urge_pattern_decoders`, `resource_plans`, `clinician_handoff_summaries`, `relapse_prevention_protocols`, `safety_plans`). Plus operational tables (`users`, `consents`, `intake_sessions`, `generated_artifacts`, `artifact_versions`, `safety_events`, `audit_logs`, …) and `fact_`/`dim_` analytics tables. Full list in the README.

### Core flow

intake → optional journal/document upload → entity extraction → safety classify → generate the 5 artifacts (relapse-risk map, urge decoder, resource plan, clinician handoff, relapse protocol) → Markdown export. The LLM/RAG service exposes one function per artifact (`generate_relapse_risk_map(user_id)`, etc.) plus `extract_recovery_entities`, `classify_safety_risk`, `embed_text`, and `generate_structured_output(prompt, schema, context)`.

### RAG separation (keep these two stores distinct)

- **Personal RAG:** the user's own intake answers, journals, documents, tracker logs, extracted patterns.
- **Curated resource RAG:** seed `docs/curated_resources.md` with general, non-medical recovery concepts (urge surfing, delay tactics, sleep-as-risk-factor, crisis escalation language). Do not fabricate clinical evidence or efficacy claims.

### Extraction contract

Every extracted entity carries: `label`, `category`, `source_text`, `source_type`, `source_id`, `confidence`, `extraction_method`, `created_at`. Artifact outputs must attach source labels (intake/journal/document/tracker/cautious inference) and a confidence level per claim.

## API surface

Routes are grouped: system (`/health`), user/intake (`/me`, `/consent`, `/intake/*`), journal, documents, extraction (`/extract/*`), safety (`/safety/classify`, `/safety/events`), artifacts (`POST .../generate` + `GET .../latest` per artifact type), tracker, and export (`/export/*/markdown`). Full endpoint list in the README.

## Commands

No build/test commands exist yet — the toolchain is not scaffolded. When establishing it, target this developer workflow (per the README's "Definition of done"): `docker compose up` brings up Postgres/pgvector, Redis, and the API; run Alembic migrations; seed a demo user and curated resources. Tests (pytest) must at minimum cover the safety classifier, intake/journal creation, document chunking, the extraction service, mock artifact generation, and the health endpoint. Record the exact commands here once they exist.

## Required docs

The deliverable includes `docs/ARCHITECTURE.md`, `docs/SAFETY.md`, `docs/DEMO_SCRIPT.md`, and `docs/MVP_LIMITATIONS.md` alongside the seeded `docs/curated_resources.md`.
