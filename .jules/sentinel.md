# Sentinel's Journal

## 2024-05-28 - [Overly Permissive CORS]
**Vulnerability:** The FastAPI application used a wildcard `"*"` for the `allow_origins` configuration in `CORSMiddleware`, allowing requests from any domain.
**Learning:** CORS was misconfigured with a wildcard in `main.py`, exposing the API to potential cross-origin attacks from malicious sites.
**Prevention:** Load a strict list of allowed origins via environment variables (e.g., `os.getenv("ALLOWED_ORIGINS")`) and default it to safe local development origins if not provided.

## 2025-03-17 - [Cross-Site Scripting (XSS) via innerHTML]
**Vulnerability:** The application was inserting unsanitized dynamic user-controlled inputs (`title`, `authors`, `topics`, etc.) directly into `div.innerHTML` inside `createBookCard` in `app/scripts.js`.
**Learning:** Using string interpolation to dynamically build HTML and insert it via `innerHTML` opens up the application to Cross-Site Scripting (XSS) if the data is not strictly sanitized.
**Prevention:** Always use a helper function to escape HTML special characters (`<`, `>`, `&`, `"`, `'`) before using string interpolation for `innerHTML`, or alternatively, use `.textContent` for safe unescaped raw text assignments.

## Daily Process Notes
* Always run `python3 -m py_compile [filename]` or `ruff check [filename]` as quick checks.
