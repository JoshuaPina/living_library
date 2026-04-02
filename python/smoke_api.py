"""Basic API smoke probe for Living Library.

Usage:
  /workspaces/living_library/.venv/bin/python python/smoke_api.py --base-url http://localhost:8000
"""

from __future__ import annotations

import argparse
import asyncio
from typing import Any

import httpx


CHECKS = [
    ("health", "GET", "/api/health", 200),
    ("topics", "GET", "/api/library/topics", 200),
    ("browse", "GET", "/api/library/browse", 200),
    ("stats", "GET", "/api/stats", 200),
    ("duplicates", "GET", "/api/duplicates", 200),
]


async def run_check(client: httpx.AsyncClient, name: str, method: str, path: str, expected: int) -> dict[str, Any]:
    response = await client.request(method, path)
    ok = response.status_code == expected
    preview = response.text[:200].replace("\n", " ")
    return {
        "name": name,
        "ok": ok,
        "status": response.status_code,
        "expected": expected,
        "path": path,
        "preview": preview,
    }


async def main_async(base_url: str, timeout: float) -> int:
    async with httpx.AsyncClient(base_url=base_url, timeout=timeout) as client:
        results = []
        for name, method, path, expected in CHECKS:
            try:
                results.append(await run_check(client, name, method, path, expected))
            except Exception as exc:  # noqa: BLE001
                results.append(
                    {
                        "name": name,
                        "ok": False,
                        "status": "EXC",
                        "expected": expected,
                        "path": path,
                        "preview": str(exc)[:200],
                    }
                )

        failed = [r for r in results if not r["ok"]]
        for r in results:
            status = "PASS" if r["ok"] else "FAIL"
            print(f"[{status}] {r['name']} {r['path']} -> {r['status']} (expected {r['expected']})")
            if not r["ok"]:
                print(f"  detail: {r['preview']}")

        if failed:
            print(f"\nSmoke probe failed: {len(failed)} check(s) failed")
            return 1

        print("\nSmoke probe passed")
        return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Run API smoke checks against a running Living Library server")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL for API server")
    parser.add_argument("--timeout", type=float, default=10.0, help="Request timeout in seconds")
    args = parser.parse_args()

    raise SystemExit(asyncio.run(main_async(args.base_url, args.timeout)))


if __name__ == "__main__":
    main()
