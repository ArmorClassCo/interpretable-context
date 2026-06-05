"""Read/verify ``.icm/baseline.json`` — the pre-overlay snapshot project-scaffold writes
BEFORE creating any ICM file in brownfield mode. The validator re-hashes against it to
prove the overlay modified no pre-existing file.

Shape:
    {
      "created": "YYYY-MM-DD",
      "paths":  [ {"path": "src/app/page.tsx", "sha256": "...", "size": 123}, ... ],
      "tool_paths": ["CLAUDE.md", "CONTEXT.md", "src/CONTEXT.md", ".icm/...", ...]
    }
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Optional, Tuple

DEFAULT_EXCLUDE = (".git",)


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_baseline(target) -> Tuple[Optional[dict], Optional[str]]:
    p = Path(target) / ".icm" / "baseline.json"
    if not p.exists():
        return None, "missing"
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001 - report any parse failure
        return None, f"unparseable JSON ({e})"
    if not isinstance(data, dict) or not isinstance(data.get("paths"), list):
        return None, "missing `paths` array"
    return data, None


def compute_snapshot(root, exclude_dirs=DEFAULT_EXCLUDE) -> dict:
    """Return {relpath: {"sha256":..., "size":...}} for every file under root."""
    root = Path(root)
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_dir() or p.is_symlink():
            continue
        rel = p.relative_to(root).as_posix()
        if any(rel == d or rel.startswith(d + "/") for d in exclude_dirs):
            continue
        out[rel] = {"sha256": sha256_file(p), "size": p.stat().st_size}
    return out
