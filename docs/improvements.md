# Living Library Improvement Log

Tracks non-bug improvements discovered during investigation.

## IMP-001 - Add reproducible runbook for local recovery

- Value: High
- Effort: Low
- Why:
  - Project has strong moving parts (FastAPI, pgvector, Supabase, local files) but no single rapid recovery flow.
- Recommendation:
  - Add `docs/runbook.md` with exact commands for setup, startup, health checks, and common failure signatures.

## IMP-002 - Add schema bootstrap automation

- Value: High
- Effort: Medium
- Why:
  - Project startup assumes DB exists and is correct.
- Recommendation:
  - Add repeatable schema bootstrap script and optional seed script to reduce configuration drift.

## IMP-003 - Add endpoint smoke test script

- Value: High
- Effort: Low
- Why:
  - Fast feedback for regressions while recovering old project state.
- Recommendation:
  - Add script that verifies health, browse/topics, semantic search contract shape, material info, and stats.
