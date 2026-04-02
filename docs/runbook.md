# Living Library Runbook

This runbook gets the app into a testable state and runs first-line probes.

## 1. Environment setup

1. Copy environment template:
   - `cp .env.example .env`
2. Edit `.env` with valid values:
   - `DATABASE_URL=postgresql://<user>:<pass>@<host>:<port>/<db>`
   - `SUPABASE_URL=<optional>`
   - `SUPABASE_KEY=<optional>`
   - `PDF_BASE_DIR=./pdfs`
3. Install dependencies:
   - `/workspaces/living_library/.venv/bin/python -m pip install -r requirements.txt`

## 2. Start API

1. Launch server:
   - `/workspaces/living_library/.venv/bin/python main.py`
2. If startup fails with missing database URL:
   - Ensure `.env` exists in project root and contains `DATABASE_URL`.

## 3. Smoke probes

Run these in a second terminal while API is running.

1. API checks:
   - `/workspaces/living_library/.venv/bin/python python/smoke_api.py --base-url http://localhost:8000`
2. Semantic check:
   - `/workspaces/living_library/.venv/bin/python test_search.py --query "machine learning" --limit 5`
3. Bug board:
   - `/workspaces/living_library/.venv/bin/python python/investigation_console.py`

## 4. UI checks

1. Open `http://localhost:8000`
2. Verify topic sidebar populates.
3. Verify semantic search returns results.
4. Verify `/app/browse.html` renders styled cards.
5. Verify `/app/viewer.html?id=<material_id>` loads document.

## 5. Common failures

1. `RuntimeError: DATABASE_URL environment variable is not set`
   - Fix `.env` and restart API.
2. Smoke script shows `All connection attempts failed`
   - API process is not running or not reachable at provided base URL.
3. Search returns empty but no errors
   - Confirm chunk and embedding data exists in `text_chunk` and `chunk_embedding`.
