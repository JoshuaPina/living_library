# Sentinel's Journal

## 2024-05-28 - [Overly Permissive CORS]
**Vulnerability:** The FastAPI application used a wildcard `"*"` for the `allow_origins` configuration in `CORSMiddleware`, allowing requests from any domain.
**Learning:** CORS was misconfigured with a wildcard in `main.py`, exposing the API to potential cross-origin attacks from malicious sites.
**Prevention:** Load a strict list of allowed origins via environment variables (e.g., `os.getenv("ALLOWED_ORIGINS")`) and default it to safe local development origins if not provided.

## Daily Process Notes
* Always run `python3 -m py_compile [filename]` or `ruff check [filename]` as quick checks.

## 2024-05-28 - [Cross-Site Scripting (XSS) via innerHTML]
**Vulnerability:** User-controlled data (like `material.title`, `node.label`, `error.message`) was being directly interpolated into DOM elements using `.innerHTML` in `app/scripts.js`, `assets/scripts.js`, and `app/viewer.html`.
**Learning:** This exposes the application to XSS attacks if a malicious user inputs scripts into fields like material titles or topics, which would then be executed in the browsers of other users viewing the application.
**Prevention:** Always sanitize dynamic, user-provided data before inserting it into `.innerHTML`. We added an `escapeHTML` helper function to replace sensitive HTML characters (`&`, `<`, `>`, `"`, `'`) with their respective HTML entities, neutralizing any potential script execution.
