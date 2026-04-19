# Sentinel's Journal

## 2024-05-28 - [Overly Permissive CORS]
**Vulnerability:** The FastAPI application used a wildcard `"*"` for the `allow_origins` configuration in `CORSMiddleware`, allowing requests from any domain.
**Learning:** CORS was misconfigured with a wildcard in `main.py`, exposing the API to potential cross-origin attacks from malicious sites.
**Prevention:** Load a strict list of allowed origins via environment variables (e.g., `os.getenv("ALLOWED_ORIGINS")`) and default it to safe local development origins if not provided.

## Daily Process Notes
* Always run `python3 -m py_compile [filename]` or `ruff check [filename]` as quick checks.

## 2024-05-29 - [Information Exposure via Error Messages]
**Vulnerability:** The FastAPI application was catching generic exceptions (`except Exception as e:`) and directly returning the raw exception string (`str(e)`) or details like file paths directly to the client via HTTP 500 responses.
**Learning:** Returning raw exception details (`str(e)`) leaks sensitive internal server information, such as database schema details, file system paths, or downstream service URLs. This can be used by an attacker to map out the system architecture and identify further vulnerabilities.
**Prevention:** Catch exceptions and log the detailed error with stack traces on the server side using the `logging` module (`logger.error("Message", exc_info=e)`). Then, return a generic, safe error message (e.g., "Internal server error") to the client.

## 2024-05-30 - [Path Traversal in PDF Download]
**Vulnerability:** The FastAPI application directly appended user-controlled input (`storage_path` from the database) to a base directory path (`PDF_BASE_DIR`) without proper validation (`PDF_BASE_DIR / storage_path`), allowing path traversal (e.g., `../../../etc/passwd`).
**Learning:** Even when path components come from a database rather than direct HTTP input, they should be treated as untrusted and validated to prevent unauthorized file system access. Using `pathlib.Path` concatenation (`/`) alone does not resolve or sanitize `../` sequences.
**Prevention:** Always validate constructed paths before using them. Resolve both the base directory and the fully constructed path using `pathlib.Path.resolve()`, and then verify that the resolved path is a subpath of the base directory using `resolved_path.is_relative_to(base_dir.resolve())`.
## 2026-04-02 - Path Traversal Vulnerability in File Delivery
**Vulnerability:** A path traversal vulnerability existed in `storage_backends.py` where a user-provided `storage_path` was concatenated with a base directory without validating if the resolved path was still within the intended base directory. This allowed a malicious user to potentially access arbitrary files on the system if `storage_path` contained sequences like `../`.
**Learning:** During conflict resolution or refactoring, security checks (like the one originally present in `main.py`) can be accidentally lost. Moreover, relying solely on Python's `Path / path_string` concatenation does not protect against directory traversal if the string contains parent directory references (`..`).
**Prevention:** Always use `pathlib.Path.resolve()` to resolve both the constructed path and the base directory, and then enforce the boundary using `constructed_path.is_relative_to(base_dir)`. This security check should be centralized in the utility function (`resolve_storage_path`) rather than scattered across endpoints.

## 2024-05-31 - [Reflected DOM XSS via Backend Error Messages]
**Vulnerability:** Frontend JavaScript code was taking raw error messages returned by the backend (such as FastAPI validation errors, which naturally reflect unsanitized user inputs that fail validation) and rendering them directly into the document using `innerHTML` (e.g., `document.body.innerHTML = \`<h1>Error</h1><p>\${error.message}</p>\`;`). This created a Reflected DOM-based Cross-Site Scripting (XSS) vulnerability.
**Learning:** Backend validation errors or API data must not be trusted when dynamically rendered on the frontend. If a framework (like FastAPI) returns the invalid user input in its error details, directly injecting that response into the DOM via `innerHTML` opens an XSS vector.
**Prevention:** Always sanitize dynamic data before inserting it into the DOM using an `escapeHTML` helper function, or use `.textContent` instead of `.innerHTML` to safely assign raw text.
