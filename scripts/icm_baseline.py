#!/usr/bin/env python3
"""Write `.icm/baseline.json` for a brownfield overlay — a snapshot of the repo's
PRE-EXISTING files (path + sha256 + size). project-scaffold runs this BEFORE creating any
ICM file; `icm validate` later re-hashes it to prove the overlay modified nothing.

    python3 scripts/icm_baseline.py <repo_dir> [created_date] > <repo_dir>/.icm/baseline.json

ICM-owned paths are excluded so the snapshot is the user's original repo only.
"""
import hashlib
import json
import sys
from pathlib import Path

EXCLUDE_TOP = {".git", ".icm"}
EXCLUDE_NAMES = {"CLAUDE.md", "CONTEXT.md", "PROJECT-BRIEF.md", ".gitkeep"}
TOOL_PATHS = [
    "CLAUDE.md", "CONTEXT.md", "PROJECT-BRIEF.md",
    ".icm/manifest.md", ".icm/README.md", ".icm/LEARNINGS-INBOX.md", ".icm/baseline.json",
]


def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: icm_baseline.py <repo_dir> [created_date]", file=sys.stderr)
        return 2
    root = Path(sys.argv[1])
    created = sys.argv[2] if len(sys.argv) > 2 else ""
    paths = []
    for p in sorted(root.rglob("*")):
        if p.is_dir() or p.is_symlink():
            continue
        rel = p.relative_to(root).as_posix()
        if rel.split("/")[0] in EXCLUDE_TOP or p.name in EXCLUDE_NAMES or rel.endswith("/CONTEXT.md"):
            continue
        paths.append({"path": rel, "sha256": _sha256(p), "size": p.stat().st_size})
    print(json.dumps({"created": created, "paths": paths, "tool_paths": TOOL_PATHS}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
