# Sentinel's Journal

## 2024-05-28 - [Overly Permissive CORS]
**Vulnerability:** The FastAPI application used a wildcard `"*"` for the `allow_origins` configuration in `CORSMiddleware`, allowing requests from any domain.
**Learning:** CORS was misconfigured with a wildcard in `main.py`, exposing the API to potential cross-origin attacks from malicious sites.
**Prevention:** Load a strict list of allowed origins via environment variables (e.g., `os.getenv("ALLOWED_ORIGINS")`) and default it to safe local development origins if not provided.

## 2024-05-28 - [Cross-Site Scripting via innerHTML]
**Vulnerability:** The frontend heavily relies on `innerHTML` to render dynamically fetched data (e.g., book titles, search snippets, error messages). Missing sanitization introduced a high-severity Cross-Site Scripting (XSS) vulnerability.
**Learning:** Raw string interpolation using template literals directly into `innerHTML` allows arbitrary script execution if the data source contains malicious scripts.
**Prevention:** Avoid `innerHTML` for dynamic content where possible by using `textContent` or `document.createElement`. If `innerHTML` is required, always sanitize dynamic variables using an `escapeHTML` helper function before interpolation.

## Daily Process Notes
* Always run `python3 -m py_compile [filename]` or `ruff check [filename]` as quick checks.
