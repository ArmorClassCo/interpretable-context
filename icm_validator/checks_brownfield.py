"""Brownfield overlay invariants — the highest-risk path.

Primary (git-independent): re-hash every file in ``.icm/baseline.json`` -> catches any
modify / delete / move of a pre-existing file, and any non-ICM file the overlay added.
Secondary (when git is present): ``git status --porcelain`` cross-check. Plus: no empty
placeholder dirs, and workspace_map sanity.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from . import baseline as bl
from .findings import Report, Severity


def _is_icm_owned(rel: str, existing_top: set) -> bool:
    """A path the overlay is allowed to add.

    ``existing_top`` is the set of pre-existing top-level directories (from the baseline).
    Files under a *newly-created* top-level dir (e.g. ``planning/``, ``ops/``) are ICM's;
    a file under an *existing* dir (e.g. ``src/``) is only ICM's if it's a CONTEXT.md /
    .gitkeep — a foreign file added under existing code must still be flagged.
    """
    if rel in ("CLAUDE.md", "CONTEXT.md", "PROJECT-BRIEF.md"):
        return True
    if rel.startswith(".icm/"):
        return True
    if rel.endswith("/CONTEXT.md"):
        return True
    if rel == ".gitkeep" or rel.endswith("/.gitkeep"):
        return True
    if "/" in rel and rel.split("/")[0] not in existing_top:
        return True  # under a newly-created workspace dir
    return False


def check(target, rt, manifest: dict, report: Report) -> None:
    target = Path(target)
    data, err = bl.load_baseline(target)
    if data is None:
        code = "BASELINE_MISSING" if err == "missing" else "BASELINE_UNPARSEABLE"
        report.add(code, Severity.ERROR, f".icm/baseline.json {err}", file=".icm/baseline.json")
        return

    baseline_paths = {e["path"]: e for e in data.get("paths", []) if isinstance(e, dict) and "path" in e}
    tool_paths = set(data.get("tool_paths", []))
    wsmap = manifest.get("workspace_map")
    existing_top = {rel.split("/")[0] for rel in baseline_paths if "/" in rel}

    # 1. pre-existing files unchanged ------------------------------------
    for rel, entry in baseline_paths.items():
        f = target / rel
        if not f.exists():
            report.add("BROWNFIELD_SOURCE_DELETED", Severity.ERROR,
                       f"pre-existing file `{rel}` is missing (moved or deleted)", file=rel)
            continue
        if bl.sha256_file(f) != entry.get("sha256"):
            report.add("BROWNFIELD_SOURCE_MODIFIED", Severity.ERROR,
                       f"pre-existing file `{rel}` was modified by the overlay", file=rel)

    # 2. only ICM files were added ---------------------------------------
    for rel in bl.compute_snapshot(target):
        if rel in baseline_paths or rel in tool_paths or _is_icm_owned(rel, existing_top):
            continue
        report.add("BROWNFIELD_UNTRACKED_NONICM", Severity.ERROR,
                   f"overlay added a non-ICM file `{rel}`", file=rel)

    # 3. workspace_map sanity --------------------------------------------
    if wsmap is None:
        report.add("WORKSPACE_MAP_MISSING", Severity.ERROR,
                   "brownfield manifest has no workspace_map block", file=".icm/manifest.md")
    else:
        for ws, dirs in wsmap.items():
            if (target / ws / "CONTEXT.md").exists() and not dirs:
                report.add("WORKSPACE_DIR_UNMAPPED", Severity.ERROR,
                           f"workspace `{ws}` has a CONTEXT.md but no existing-dir mapping",
                           file=".icm/manifest.md")
            for d in dirs:
                if not (target / d).exists():
                    report.add("WORKSPACE_DIR_NONEXISTENT", Severity.ERROR,
                               f"workspace_map `{ws} -> {d}` points at a non-existent directory",
                               file=".icm/manifest.md")

    # 4. no empty placeholder dirs the overlay created -------------------
    pre_dirs = set()
    for rel in baseline_paths:
        parts = rel.split("/")
        for i in range(1, len(parts)):
            pre_dirs.add("/".join(parts[:i]))
    for p in sorted(target.rglob("*")):
        if not p.is_dir():
            continue
        rel = p.relative_to(target).as_posix()
        if rel.startswith(".git") or rel in pre_dirs:
            continue
        if not any(p.iterdir()):
            report.add("OVERLAY_EMPTY_PLACEHOLDER", Severity.WARN,
                       f"overlay created empty placeholder dir `{rel}/`", file=rel)

    # 5. git cross-check (optional) --------------------------------------
    _git_crosscheck(target, tool_paths, existing_top, report)


def _git_crosscheck(target: Path, tool_paths, existing_top, report: Report) -> None:
    try:
        inside = subprocess.run(["git", "-C", str(target), "rev-parse", "--is-inside-work-tree"],
                                capture_output=True, text=True, timeout=10)
        if inside.returncode != 0 or inside.stdout.strip() != "true":
            return
        # scope to the target subtree (`.`) so a fixture nested in another repo doesn't
        # pick up the enclosing repo's changes
        st = subprocess.run(["git", "-C", str(target), "status", "--porcelain", "."],
                            capture_output=True, text=True, timeout=10)
    except Exception:  # noqa: BLE001 - git absent / not a repo -> skip silently
        return
    for line in st.stdout.splitlines():
        if not line.strip():
            continue
        status, path = line[:2], line[3:].strip().strip('"')
        if "->" in path:
            path = path.split("->")[-1].strip()
        if path in tool_paths or _is_icm_owned(path, existing_top):
            continue
        if any(c in status for c in ("M", "D", "R")):
            report.add("GIT_TRACKED_MODIFIED", Severity.WARN,
                       f"git reports non-ICM tracked file `{path}` as `{status.strip()}`", file=path)
