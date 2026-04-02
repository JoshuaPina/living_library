"""Render bug priorities from docs/bugs.md using Rich.

Usage:
  /workspaces/living_library/.venv/bin/python python/investigation_console.py
"""

from __future__ import annotations

from pathlib import Path
from rich.console import Console
from rich.table import Table

BUGS_PATH = Path(__file__).resolve().parents[1] / "docs" / "bugs.md"


def parse_bug_blocks(content: str) -> list[dict[str, str]]:
    blocks: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for raw_line in content.splitlines():
        line = raw_line.strip()

        if line.startswith("## BUG-"):
            if current:
                blocks.append(current)
            current = {"title": line.replace("## ", "", 1)}
            continue

        if not current:
            continue

        if line.startswith("- Status:"):
            current["status"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Severity:"):
            current["severity"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Frequency:"):
            current["frequency"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Effort to fix:"):
            current["effort"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Impact on users:"):
            current["impact"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Confidence in fix:"):
            current["confidence"] = line.split(":", 1)[1].strip()
        elif line.startswith("- Priority score:"):
            current["priority"] = line.split(":", 1)[1].strip()

    if current:
        blocks.append(current)

    return blocks


def main() -> None:
    console = Console()

    if not BUGS_PATH.exists():
        console.print(f"[red]Missing bug log:[/red] {BUGS_PATH}")
        raise SystemExit(1)

    bugs = parse_bug_blocks(BUGS_PATH.read_text(encoding="utf-8"))
    if not bugs:
        console.print("[yellow]No bugs found in docs/bugs.md[/yellow]")
        return

    bugs = sorted(bugs, key=lambda b: int(b.get("priority", "0")), reverse=True)

    console.print("\nTop bugs by priority:")
    for idx, bug in enumerate(bugs, start=1):
        console.print(
            f"{idx}. {bug.get('title', 'N/A')} | "
            f"status={bug.get('status', 'N/A')} | "
            f"priority={bug.get('priority', '-')}"
        )

    table = Table(title="Living Library Bug Priority Board")
    table.add_column("Bug", style="cyan", no_wrap=True)
    table.add_column("Status", style="magenta")
    table.add_column("S")
    table.add_column("F")
    table.add_column("E")
    table.add_column("I")
    table.add_column("C")
    table.add_column("Priority", style="bold green")

    for bug in bugs:
        table.add_row(
            bug.get("title", "N/A"),
            bug.get("status", "N/A"),
            bug.get("severity", "-"),
            bug.get("frequency", "-"),
            bug.get("effort", "-"),
            bug.get("impact", "-"),
            bug.get("confidence", "-"),
            bug.get("priority", "-"),
        )

    console.print(table)


if __name__ == "__main__":
    main()
