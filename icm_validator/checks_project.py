"""`icm validate project <dir>` — registry-driven structural checks on a scaffolded
(greenfield) or overlaid (brownfield) ICM project.

Every check is mechanical. The set of required CLAUDE.md sections, the Avoid baselines,
the workspace list, and which fields are bound into the tree are all *derived from the
type's registry file* — so a new/completed type needs no change here.
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import List, Optional

from . import markdown as md
from . import registry as reg
from .findings import Report, Severity

MANIFEST_KEYS = ("type", "registry_version", "shape", "origin", "created")
_STOP = {
    "with", "that", "this", "your", "from", "they", "them", "what", "when", "will",
    "into", "main", "thing", "using", "make", "need", "want", "have", "once", "also",
    "built", "app", "the", "and", "for", "you",
}


def _rel(path: Path, root: Path) -> str:
    try:
        return os.path.relpath(path, root)
    except ValueError:
        return str(path)


def _generated_markdown(target: Path) -> List[Path]:
    files: List[Path] = []
    cl = target / "CLAUDE.md"
    if cl.exists():
        files.append(cl)
    for p in sorted(target.glob("**/CONTEXT.md")):
        s = str(p)
        if "/.git/" not in s and "/node_modules/" not in s:
            files.append(p)
    icm = target / ".icm"
    if icm.is_dir():
        files += sorted(icm.glob("*.md"))
    return files


def parse_brief_manifest(text: str) -> dict:
    """Field values from a PROJECT-BRIEF.md Structure Manifest (`- id: value [prov]`)."""
    body = md.h2_section_body(text, "Structure Manifest")
    if body is None:
        return {}
    out = {}
    for b in md.bullets(body):
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", b)
        if m:
            val = re.sub(r"\s*\[[^\]]*\]\s*$", "", m.group(2)).strip()  # strip [provenance]
            out[m.group(1)] = val
    return out


def _needle(value: str) -> Optional[str]:
    words = [w for w in re.findall(r"[A-Za-z0-9.]+", value)
             if len(w) >= 4 and w.lower() not in _STOP]
    return max(words, key=len) if words else None


def validate_project(target, registry_dir: Optional[str] = None) -> Report:
    target = Path(target)
    report = Report(subcommand="validate-project", target=str(target))

    # --- manifest ---------------------------------------------------------
    manifest_path = target / ".icm" / "manifest.md"
    manifest: dict = {}
    if not manifest_path.exists():
        report.add("MANIFEST_MISSING", Severity.ERROR, ".icm/manifest.md is missing",
                   file=".icm/manifest.md")
    else:
        manifest = md.parse_manifest(manifest_path.read_text(encoding="utf-8"))
        for k in MANIFEST_KEYS:
            if k not in manifest:
                report.add("MANIFEST_FIELD_MISSING", Severity.ERROR,
                           f"manifest missing required key `{k}`", file=".icm/manifest.md")

    origin = str(manifest.get("origin", "greenfield")).strip() or "greenfield"
    report.origin = origin

    rt: Optional[reg.RegistryType] = None
    type_name = manifest.get("type")
    if type_name:
        try:
            rt = reg.load_type(str(type_name), registry_dir)
        except reg.RegistryError:
            report.add("MANIFEST_TYPE_UNKNOWN", Severity.ERROR,
                       f"manifest type `{type_name}` has no registry file", file=".icm/manifest.md")
    lenient = bool(rt and rt.is_stub)

    if rt:
        rv = str(manifest.get("registry_version", "")).strip()
        if rv and rv not in (rt.version, "unknown"):
            report.add("MANIFEST_VERSION_MISMATCH", Severity.WARN,
                       f"scaffolded against registry v{rv}, live registry is v{rt.version}",
                       file=".icm/manifest.md")
        sh = str(manifest.get("shape", "")).strip()
        if sh and sh != rt.shape:
            report.add("MANIFEST_SHAPE_MISMATCH", Severity.ERROR,
                       f"manifest shape `{sh}` != registry shape `{rt.shape}`", file=".icm/manifest.md")

    # --- .icm marker files ------------------------------------------------
    if not (target / ".icm" / "README.md").exists():
        report.add("ICM_README_MISSING", Severity.ERROR, ".icm/README.md is missing", file=".icm/README.md")
    if not (target / ".icm" / "LEARNINGS-INBOX.md").exists():
        report.add("ICM_INBOX_MISSING", Severity.ERROR, ".icm/LEARNINGS-INBOX.md is missing",
                   file=".icm/LEARNINGS-INBOX.md")

    gen_files = _generated_markdown(target)

    # --- unresolved slots (highest-value check) ---------------------------
    for f in gen_files:
        rel = _rel(f, target)
        for tok, ln in md.snake_slots_with_lines(f.read_text(encoding="utf-8")):
            report.add("SLOT_UNRESOLVED", Severity.ERROR,
                       f"unfilled template slot `{{{tok}}}`", file=rel, line=ln)

    # --- CLAUDE.md (L0) ---------------------------------------------------
    _check_claude(target, rt, lenient, report)

    # --- root CONTEXT.md (L1) ---------------------------------------------
    _check_root_context(target, report)

    # --- workspaces + maps_to bindings (skip for stub-scaffolded minimal) -
    if rt and not lenient:
        _check_workspaces(target, rt, manifest, origin, report)
        _check_bindings(target, rt, gen_files, report)

    # --- brownfield overlay invariants ------------------------------------
    if origin == "brownfield":
        from . import checks_brownfield
        checks_brownfield.check(target, rt, manifest, report)

    return report


def _check_claude(target: Path, rt, lenient: bool, report: Report) -> None:
    path = target / "CLAUDE.md"
    if not path.exists():
        report.add("CLAUDE_MISSING", Severity.ERROR, "CLAUDE.md is missing", file="CLAUDE.md")
        return
    text = path.read_text(encoding="utf-8")
    if md.line_count(text) >= 200:
        report.add("CLAUDE_TOO_LONG", Severity.ERROR,
                   f"CLAUDE.md is {md.line_count(text)} lines (L0 must stay < 200)", file="CLAUDE.md")
    if md.has_routing_table(text):
        report.add("L0_HAS_ROUTING_TABLE", Severity.ERROR,
                   "CLAUDE.md contains a routing table (routing belongs in CONTEXT.md)", file="CLAUDE.md")

    if rt and not lenient:
        have = {t.lower() for t in md.h2_titles(text)}
        for heading in rt.claude_headings():
            if heading.lower() not in have:
                report.add("CLAUDE_SECTION_MISSING", Severity.ERROR,
                           f"CLAUDE.md missing required section `## {heading}`", file="CLAUDE.md")

        avoid = md.h2_section_body(text, "Avoid")
        if avoid is None or not md.bullets(avoid):
            report.add("AVOID_EMPTY", Severity.ERROR, "CLAUDE.md Avoid section is empty", file="CLAUDE.md")
        else:
            if not re.search(r"(?im)^###\s+hard\b", avoid):
                report.add("AVOID_NO_HARD", Severity.WARN,
                           "CLAUDE.md Avoid has no `### Hard constraints` subsection", file="CLAUDE.md")
            rendered = "\n".join(md.bullets(avoid)).lower()
            for baseline in rt.avoid_baseline_bullets():
                key = re.sub(r"\s+", " ", baseline.lower())[:40]
                if key and key not in re.sub(r"\s+", " ", rendered):
                    report.add("AVOID_NO_BASELINE", Severity.WARN,
                               f"CLAUDE.md Avoid missing baseline guardrail: {baseline[:50]}…", file="CLAUDE.md")

        commands = md.h2_section_body(text, "Commands")
        tables = md.parse_pipe_tables(commands) if commands else []
        if not commands or not tables:
            report.add("COMMANDS_MISSING", Severity.ERROR, "CLAUDE.md has no Commands table", file="CLAUDE.md")
        else:
            for row in tables[0]["rows"]:
                cells = list(row.values())
                if len(cells) >= 2 and not cells[1].strip():
                    report.add("COMMANDS_EMPTY_CELL", Severity.WARN,
                               f"Commands row `{cells[0]}` has an empty command cell", file="CLAUDE.md")


def _check_root_context(target: Path, report: Report) -> None:
    path = target / "CONTEXT.md"
    if not path.exists():
        report.add("L1_MISSING", Severity.ERROR, "root CONTEXT.md is missing", file="CONTEXT.md")
        return
    text = path.read_text(encoding="utf-8")
    if not md.has_routing_table(text):
        report.add("L1_NOT_ROUTER", Severity.ERROR,
                   "root CONTEXT.md has no task->workspace routing table", file="CONTEXT.md")
    if md.has_folder_map_or_naming(text):
        report.add("L1_HAS_FOLDER_MAP", Severity.ERROR,
                   "root CONTEXT.md contains a folder map / naming (belongs in CLAUDE.md)", file="CONTEXT.md")
    # routing targets resolve
    for t in md.parse_pipe_tables(text):
        if not md.looks_like_routing_table(t["header"]):
            continue
        for row in t["rows"]:
            for cell in row.values():
                for ref in re.findall(r"`([A-Za-z0-9_./-]+)`", cell):
                    if ref.endswith("/CONTEXT.md") or "/" in ref or ref.endswith(".md"):
                        if not (target / ref).exists() and not (target / ref.rstrip("/")).exists():
                            report.add("ROUTER_TARGET_MISSING", Severity.ERROR,
                                       f"routing target `{ref}` does not resolve", file="CONTEXT.md")


def _check_workspaces(target: Path, rt, manifest: dict, origin: str, report: Report) -> None:
    if origin == "brownfield":
        wsmap = manifest.get("workspace_map") or {}
        workspaces = list(wsmap.keys())
    else:
        workspaces = rt.workspace_dirs()
    for ws in workspaces:
        ctx = target / ws / "CONTEXT.md"
        if not ctx.exists():
            report.add("WORKSPACE_CONTEXT_MISSING", Severity.ERROR,
                       f"workspace `{ws}/` has no CONTEXT.md", file=f"{ws}/CONTEXT.md")
        if origin == "greenfield":
            wsdir = target / ws
            if wsdir.is_dir():
                for sub in wsdir.iterdir():
                    if sub.is_dir() and not any(sub.iterdir()):
                        report.add("WORKSPACE_EMPTY_PLACEHOLDER", Severity.WARN,
                                   f"empty dir `{_rel(sub, target)}` has no .gitkeep", file=_rel(sub, target))


def _check_bindings(target: Path, rt, gen_files: List[Path], report: Report) -> None:
    brief_path = target / "PROJECT-BRIEF.md"
    if not brief_path.exists():
        return  # binding check needs the brief's field values
    values = parse_brief_manifest(brief_path.read_text(encoding="utf-8"))
    tree_text = "\n".join(f.read_text(encoding="utf-8") for f in gen_files).lower()
    templated = rt.field_ids() & (
        set(md.snake_placeholders(rt.section_body(6))) | set(md.snake_placeholders(rt.section_body(7)))
    )
    for row in rt.required_fields():
        fid = row["id"]
        # MAPSTO_TARGET_MISSING: named generated-contract files should exist
        for ref in re.findall(r"([A-Za-z0-9_./-]+/CONTEXT\.md|CLAUDE\.md)", row["maps_to"]):
            if not (target / ref).exists():
                report.add("MAPSTO_TARGET_MISSING", Severity.WARN,
                           f"`{fid}` maps_to `{ref}` which does not exist", file="PROJECT-BRIEF.md")
        # MAPSTO_VALUE_ABSENT: only for fields the templates actually place into the tree
        if fid not in templated:
            continue
        needle = _needle(values.get(fid, ""))
        if needle and needle.lower() not in tree_text:
            report.add("MAPSTO_VALUE_ABSENT", Severity.ERROR,
                       f"required field `{fid}` value (`{needle}`) is absent from the generated tree",
                       file="PROJECT-BRIEF.md")
