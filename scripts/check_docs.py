#!/usr/bin/env python3
"""Repository sanity checks run in CI (deterministic, offline).

Checks:
1. All required files exist.
2. Every internal (relative) link in the Markdown docs resolves.
3. No merge-conflict markers in tracked text files.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "docs/PROPOSAL.md",
    "docs/TECHNICAL_WHITEPAPER.md",
    "docs/BUDGET.md",
    "docs/RESEARCH.md",
    "docs/PROPOSAL_CHECKLIST.md",
    "docs/ROADMAP.md",
    "poc/README.md",
    "poc/requirements.txt",
    "poc/requirements-dev.txt",
    "poc/src/pirlight/__init__.py",
    "poc/src/pirlight/chain.py",
    "poc/src/pirlight/pir.py",
    "poc/src/pirlight/client.py",
    "poc/src/pirlight/metrics.py",
    "poc/src/pirlight/demo.py",
    "poc/tests/test_pir.py",
    "poc/tests/test_client.py",
    "scripts/check_docs.py",
    ".github/workflows/ci.yml",
    "pyproject.toml",
]

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
# Built from repeated characters so this file does not contain the markers
# it searches for.
CONFLICT_MARKERS = ("<" * 7, ">" * 7)
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__"}
TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".toml", ".txt"}


def markdown_files() -> list[Path]:
    return [
        p
        for p in ROOT.rglob("*.md")
        if not any(part in SKIP_DIRS for part in p.parts)
    ]


def check_links() -> list[str]:
    errors: list[str] = []
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            resolved = (path.parent / path_part).resolve()
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}: broken link -> {target}")
    return errors


def check_conflict_markers() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for marker in CONFLICT_MARKERS:
            if marker in text:
                errors.append(f"{path.relative_to(ROOT)}: merge conflict marker {marker!r}")
    return errors


def main() -> int:
    errors: list[str] = []
    missing = [f for f in REQUIRED if not (ROOT / f).exists()]
    if missing:
        errors.append(f"missing required files: {missing}")
    errors.extend(check_links())
    errors.extend(check_conflict_markers())
    if errors:
        print("DOC CHECK FAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print(
        f"DOC CHECK OK: {len(REQUIRED)} required files present,"
        f" all internal links resolve, no conflict markers"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
