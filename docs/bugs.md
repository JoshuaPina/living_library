# Living Library Bug Log

This file tracks confirmed bugs using a 5-metric system.

Metric scale: 1 (low) to 5 (high).
Priority score formula:
- `priority = (severity + frequency + impact_on_users + confidence_in_fix) - effort_to_fix`
- Higher scores are addressed first.

## BUG-001 - Missing DATABASE_URL bootstrap guidance blocks startup recovery

- Status: RESOLVED
- Component: Backend startup/config
- Affected area: API server boot path
- Evidence:
  - Runtime command: `/workspaces/living_library/.venv/bin/python main.py`
  - Error: `RuntimeError: DATABASE_URL environment variable is not set. The API cannot start without it.`
- Reproduction steps:
1. Ensure no `.env` file is present in project root.
2. Run `/workspaces/living_library/.venv/bin/python main.py`.
3. Observe startup crash with RuntimeError.
- Root cause (current understanding):
  - Startup hard-fails by design when `DATABASE_URL` is missing in environment.
  - This is expected behavior, but it is a practical blocker for project recovery due to no `.env.example` or bootstrap guardrails.
- Suggested fix:
  - Add `.env.example` with required variables. (Implemented)
  - Add startup diagnostic to explicitly print expected URL format and quick next steps. (Implemented)
- Metrics:
  - Severity: 5
  - Frequency: 5
  - Effort to fix: 1
  - Impact on users: 5
  - Confidence in fix: 5
  - Priority score: 19

## BUG-002 - Browse page loads wrong stylesheet path

- Status: RESOLVED
- Component: Frontend
- Affected area: Browse UI
- Evidence:
  - File: `app/browse.html`
  - Current link tag: `<link rel="stylesheet" href="/app/styles.css">`
  - Repository has `assets/styles.css`; no `app/styles.css` file exists.
- Reproduction steps:
1. Open `/app/browse.html`.
2. Open browser dev tools network panel.
3. Observe stylesheet request for `/app/styles.css` returns 404.
4. Page renders unstyled or partially styled.
- Root cause (current understanding):
  - Mismatch between asset location and referenced path.
- Suggested fix:
  - Change stylesheet link to `/assets/styles.css`. (Implemented)
- Metrics:
  - Severity: 3
  - Frequency: 5
  - Effort to fix: 1
  - Impact on users: 4
  - Confidence in fix: 5
  - Priority score: 16

## BUG-003 - Inconsistent runtime logging in backend hinders debugging

- Status: RESOLVED
- Component: Backend observability
- Affected area: Startup, PDF retrieval, error handling
- Evidence:
  - `main.py` currently mixes raw `print()` statements for warnings/errors.
  - No structured context for key failures (material_id, provider, file path).
- Reproduction steps:
1. Trigger failures in PDF fetch paths or missing Supabase setup.
2. Review console output.
3. Observe ad-hoc logs without consistent levels/metadata.
- Root cause (current understanding):
  - No centralized logger usage in these code paths.
- Suggested fix:
  - Add module logger and replace `print()` with level-based logging. (Implemented)
- Metrics:
  - Severity: 3
  - Frequency: 4
  - Effort to fix: 2
  - Impact on users: 3
  - Confidence in fix: 5
  - Priority score: 13

## BUG-004 - Runtime smoke tests blocked by missing active environment variables in workspace

- Status: BLOCKED
- Component: Investigation runtime setup
- Affected area: API smoke test phase (health/search/pdf/stats)
- Evidence:
  - `.env` file is absent in project root.
  - Shell checks report `DATABASE_URL` and Supabase vars unset.
  - API startup command fails before endpoints can be exercised.
  - `python/smoke_api.py` results: health/topics/browse/stats/duplicates all failed with `All connection attempts failed`.
  - 2026-03-25 ready-check repeated same result in active probe terminal (`.env` missing, env vars unset).
  - 2026-03-25 live probe attempt: API startup failed with `RuntimeError: DATABASE_URL environment variable is not set`.
- Reproduction steps:
1. In current workspace shell, run `[[ -n "$DATABASE_URL" ]] && echo set || echo unset`.
2. Run `/workspaces/living_library/.venv/bin/python main.py`.
3. Observe startup failure due missing database URL.
- Root cause (current understanding):
  - Required runtime secrets are not configured in this workspace session.
- Suggested fix:
  - Create `.env` from `.env.example` and populate actual credentials.
  - Re-run startup and endpoint probes.
- Metrics:
  - Severity: 4
  - Frequency: 5
  - Effort to fix: 2
  - Impact on users: 4
  - Confidence in fix: 5
  - Priority score: 16

## BUG-005 - Semantic probe script crashes with AttributeError when DATABASE_URL is missing

- Status: RESOLVED
- Component: Testing/probes
- Affected area: Local semantic search verification workflow
- Evidence:
  - Running `test_search.py` previously raised: `AttributeError: 'NoneType' object has no attribute 'startswith'`.
- Reproduction steps:
1. Ensure no DATABASE_URL is set.
2. Run `/workspaces/living_library/.venv/bin/python test_search.py`.
3. Observe crash before any useful guidance.
- Root cause (current understanding):
  - Script assumed `DATABASE_URL` is always non-null and called `.startswith` unguarded.
- Suggested fix:
  - Add explicit env validation and readable error path. (Implemented)
  - Add `--query` and `--limit` args for reusable probes. (Implemented)
- Metrics:
  - Severity: 3
  - Frequency: 5
  - Effort to fix: 1
  - Impact on users: 3
  - Confidence in fix: 5
  - Priority score: 15
