from __future__ import annotations

from python.investigation_console import parse_bug_blocks


def test_parse_bug_blocks_extracts_priority_fields() -> None:
    content = """
# Living Library Bug Log

## BUG-010 - Example issue

- Status: RESOLVED
- Severity: 4
- Frequency: 2
- Effort to fix: 1
- Impact on users: 3
- Confidence in fix: 5
- Priority score: 13
"""

    bugs = parse_bug_blocks(content)

    assert len(bugs) == 1
    assert bugs[0]["title"] == "BUG-010 - Example issue"
    assert bugs[0]["status"] == "RESOLVED"
    assert bugs[0]["priority"] == "13"
