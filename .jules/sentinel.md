# Sentinel's Journal

## 2024-05-28 - [Overly Permissive CORS]
**Vulnerability:** The FastAPI application used a wildcard `"*"` for the `allow_origins` configuration in `CORSMiddleware`, allowing requests from any domain.
**Learning:** CORS was misconfigured with a wildcard in `main.py`, exposing the API to potential cross-origin attacks from malicious sites.
**Prevention:** Load a strict list of allowed origins via environment variables (e.g., `os.getenv("ALLOWED_ORIGINS")`) and default it to safe local development origins if not provided.

## Daily Process Notes
* Always run `python3 -m py_compile [filename]` or `ruff check [filename]` as quick checks.

## 2024-05-29 - [Cross-Site Scripting (XSS) in DOM Manipulation]
**Vulnerability:** User-provided or database-derived data (e.g., titles, authors, error messages) was directly inserted into the DOM using `innerHTML` without sanitization.
**Learning:** This codebase relies on native DOM manipulation. Using `innerHTML` with unsanitized inputs allows an attacker to inject arbitrary scripts (XSS).
**Prevention:** Use an `escapeHTML` helper function to sanitize all dynamic data before using it in `innerHTML`, or prefer safe properties like `textContent` when assigning raw text.
