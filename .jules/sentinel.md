# Sentinel's Journal

## 2024-05-28 - [Overly Permissive CORS]
**Vulnerability:** The FastAPI application used a wildcard `"*"` for the `allow_origins` configuration in `CORSMiddleware`, allowing requests from any domain.
**Learning:** CORS was misconfigured with a wildcard in `main.py`, exposing the API to potential cross-origin attacks from malicious sites.
**Prevention:** Load a strict list of allowed origins via environment variables (e.g., `os.getenv("ALLOWED_ORIGINS")`) and default it to safe local development origins if not provided.

## 2024-05-28 - [Information Disclosure in Error Messages]
**Vulnerability:** The API returned raw exception strings (`str(e)`) to the client when a 500 Internal Server Error occurred, exposing sensitive internal details like database query structures or connection strings.
**Learning:** Returning `str(e)` directly in an API response can unintentionally leak sensitive backend implementation details. Error handling should log the details server-side and return generic error messages to the client.
**Prevention:** Never use `str(e)` directly in user-facing error responses. Use generic messages like "Internal server error" for 500 responses and log the detailed exception server-side using a logging framework.

## Daily Process Notes
* Always run `python3 -m py_compile [filename]` or `ruff check [filename]` as quick checks.
