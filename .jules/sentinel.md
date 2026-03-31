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

## 2024-05-30 - [Path Traversal in File Download]
**Vulnerability:** The `get_pdf_page` endpoint in `main.py` allowed path traversal attacks because it joined `PDF_BASE_DIR` with a `storage_path` from the database without properly validating that the resulting path remained within `PDF_BASE_DIR`. An attacker could potentially bypass the intended directory.
**Learning:** Even if file paths originate from a database rather than direct user input, they should be treated as untrusted and rigorously validated before being used in file system operations to prevent arbitrary file access.
**Prevention:** Use `pathlib.Path.resolve().relative_to(base_dir.resolve())` to ensure any constructed path is strictly contained within the intended base directory. If a `ValueError` is raised, reject the request.
