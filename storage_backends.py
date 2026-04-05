"""Storage backend helpers for PDF assets.

Google Drive is handled as a path-based provider so PDFs can live in a synced
folder while the existing page-by-page rendering flow stays unchanged.
"""

from __future__ import annotations

import os
from pathlib import Path


PATH_BASED_STORAGE_PROVIDERS = {"local", "onedrive", "google_drive"}


def is_path_based_storage(storage_provider: str) -> bool:
    """Return True when the provider is backed by the filesystem."""

    return storage_provider in PATH_BASED_STORAGE_PROVIDERS


def get_storage_root(storage_provider: str, default_root: Path) -> Path:
    """Return the filesystem root for a path-based storage provider."""

    if storage_provider == "google_drive":
        return Path(os.getenv("GOOGLE_DRIVE_BASE_DIR", os.getenv("PDF_BASE_DIR", default_root)))

    if storage_provider == "onedrive":
        return Path(os.getenv("ONEDRIVE_BASE_DIR", os.getenv("PDF_BASE_DIR", default_root)))

    return Path(os.getenv("PDF_BASE_DIR", default_root))


def resolve_storage_path(storage_provider: str, storage_path: str, default_root: Path) -> Path:
    """Resolve a storage-relative path to an absolute filesystem path."""

    storage_root = get_storage_root(storage_provider, default_root)
    resolved_root = storage_root.resolve()

    # Strip leading slash to prevent it from acting as absolute root
    clean_path = storage_path.lstrip("/")

    resolved_path = (storage_root / clean_path).resolve()
    if not resolved_path.is_relative_to(resolved_root):
        raise ValueError(f"Path traversal attempt blocked: {storage_path}")

    return resolved_path
