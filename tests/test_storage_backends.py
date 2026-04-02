from __future__ import annotations

from pathlib import Path

from storage_backends import is_path_based_storage, resolve_storage_path


def test_google_drive_is_path_based() -> None:
    assert is_path_based_storage("google_drive") is True


def test_supabase_is_not_path_based() -> None:
    assert is_path_based_storage("supabase") is False


def test_resolve_storage_path_uses_google_drive_root(monkeypatch) -> None:
    monkeypatch.setenv("GOOGLE_DRIVE_BASE_DIR", "/tmp/google-drive")

    path = resolve_storage_path("google_drive", "books/example.pdf", Path("/fallback"))

    assert path == Path("/tmp/google-drive/books/example.pdf")
