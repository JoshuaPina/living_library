# Sentinel's Journal

## 2024-05-28 - [Overly Permissive CORS]
**Vulnerability:** The FastAPI application used a wildcard `"*"` for the `allow_origins` configuration in `CORSMiddleware`, allowing requests from any domain.
**Learning:** CORS was misconfigured with a wildcard in `main.py`, exposing the API to potential cross-origin attacks from malicious sites.
**Prevention:** Load a strict list of allowed origins via environment variables (e.g., `os.getenv("ALLOWED_ORIGINS")`) and default it to safe local development origins if not provided.

## Daily Process Notes
* Always run `python3 -m py_compile [filename]` or `ruff check [filename]` as quick checks.

## 2024-05-29 - [Path Traversal in PDF Download]
**Vulnerability:** The `/api/pdf/{material_id}/page/{page_num}` endpoint used user-supplied `storage_path` directly to construct the file path (`PDF_BASE_DIR / storage_path`) without validation, allowing directory traversal attacks (e.g., passing `../etc/passwd` to access arbitrary system files).
**Learning:** Concatenating user-controlled input with a base directory using `pathlib` is unsafe because `pathlib` normalizes `..` sequences and will traverse outside the intended directory if not explicitly checked.
**Prevention:** Always use `path.resolve()` on both the base directory and the constructed file path, and then verify that the constructed path is a subpath of the base directory using `constructed_path.relative_to(base_dir.resolve())`. If this raises a `ValueError`, reject the request as it indicates a directory traversal attempt.
