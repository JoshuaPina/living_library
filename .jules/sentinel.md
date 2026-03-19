# Sentinel's Journal

## 2024-05-28 - [Overly Permissive CORS]
**Vulnerability:** The FastAPI application used a wildcard `"*"` for the `allow_origins` configuration in `CORSMiddleware`, allowing requests from any domain.
**Learning:** CORS was misconfigured with a wildcard in `main.py`, exposing the API to potential cross-origin attacks from malicious sites.
**Prevention:** Load a strict list of allowed origins via environment variables (e.g., `os.getenv("ALLOWED_ORIGINS")`) and default it to safe local development origins if not provided.

## Daily Process Notes
* Always run `python3 -m py_compile [filename]` or `ruff check [filename]` as quick checks.

## 2024-05-24 - High Priority Cross-Site Scripting (XSS) Vulnerability in Search Results
**Vulnerability:** A Cross-Site Scripting (XSS) vulnerability was found in `assets/scripts.js` where user-controlled text (`result.material_id`, `result.title`, `result.page_number`, and `snippet` from the semantic search response) was directly injected into the DOM via `innerHTML` without escaping.
**Learning:** Although an `escapeHTML` function was defined and available in the script, and even used in other files like `app/scripts.js`, the developer forgot to wrap dynamic variables with it when rendering semantic search results in `assets/scripts.js`. This shows that having sanitization utilities is not enough—they must be consistently applied anywhere `innerHTML` or similar risky DOM manipulation methods are used.
**Prevention:** To prevent this, always ensure variables are wrapped in an HTML escaping function (like `escapeHTML`) when using template literals with `.innerHTML`. Alternatively, prefer assigning to `.textContent` when inserting plain text or rely on frameworks that handle escaping automatically by default.
