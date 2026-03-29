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

## 2024-10-24 - [Path Traversal in File Downloads]
**Vulnerability:** The application was constructing file paths by directly joining a base directory with user-supplied or database-supplied `storage_path` values without resolving them.
**Learning:** This could allow a malicious actor (who gained control over `storage_path` metadata) to construct a path like `../../../../etc/passwd`, potentially exposing arbitrary files on the filesystem. This is a critical risk for systems reading dynamically determined files.
**Prevention:** Always use `pathlib.Path.resolve()` to expand out any relative path segments, and strictly verify that the resulting absolute path is a child of the intended base directory using `path.relative_to(base_dir.resolve())`.
