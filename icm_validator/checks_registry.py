"""`icm lint` — validate a registry type file against the 10-section FORMAT SPEC.

Strict for ``status: complete`` types; lenient for ``status: stub`` (reports TODO
sections as info, never errors — unless ``--strict``). All checks are mechanical.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional

from . import markdown as md
from . import registry as reg
from .findings import Report, Severity


def lint_type(rt: reg.RegistryType, strict: bool, report: Report,
              known_index_types: Optional[set] = None) -> None:
    path = str(rt.path)
    fm = rt.frontmatter
    if fm is None:
        report.add("FM_MISSING", Severity.ERROR, "frontmatter missing or unparseable", file=path)
        report.registry_failure = True
        return

    for key in ("type", "version", "shape", "status", "match_signals"):
        if key not in fm:
            report.add("FM_KEY_MISSING", Severity.ERROR, f"missing frontmatter key `{key}`", file=path)

    if str(fm.get("type", "")).strip() != rt.path.stem:
        report.add("FM_TYPE_STEM_MISMATCH", Severity.ERROR,
                   f"`type: {fm.get('type')}` != filename stem `{rt.path.stem}`", file=path)
    if not re.fullmatch(r"\d+", str(fm.get("version", "")).strip()):
        report.add("FM_VERSION_NOT_INT", Severity.ERROR,
                   f"`version` must be an integer (got {fm.get('version')!r})", file=path)
    if str(fm.get("shape", "")).strip() not in reg.VALID_SHAPES:
        report.add("FM_SHAPE_INVALID", Severity.ERROR,
                   f"`shape` must be one of {sorted(reg.VALID_SHAPES)}", file=path)
    status = str(fm.get("status", "")).strip()
    if status not in reg.VALID_STATUS:
        report.add("FM_STATUS_INVALID", Severity.ERROR,
                   f"`status` must be one of {sorted(reg.VALID_STATUS)}", file=path)
    ms = fm.get("match_signals")
    if not ms or (isinstance(ms, list) and len(ms) == 0):
        report.add("FM_MATCH_SIGNALS_EMPTY", Severity.WARN, "`match_signals` is empty", file=path)

    is_stub = status == "stub"
    lenient = is_stub and not strict
    present = set(rt.sections.keys())

    # --- required sections ------------------------------------------------
    required = reg.STUB_REQUIRED if lenient else reg.COMPLETE_REQUIRED
    for num in sorted(required):
        if num not in present:
            report.add("SPEC_SECTION_MISSING", Severity.ERROR,
                       f"missing §{num} ({reg.SECTION_TITLES[num]})", file=path)
    if not lenient:
        nums = list(rt.order)
        if nums != sorted(nums):
            report.add("SPEC_SECTION_ORDER", Severity.ERROR,
                       f"sections out of order: {nums}", file=path)

    # --- stub reporting / strict TODO rejection ---------------------------
    if is_stub:
        todo: List[int] = []
        for num in sorted(reg.COMPLETE_REQUIRED):
            body = rt.sections.get(num, (None, ""))[1]
            if num not in present or "TODO" in body or body.strip() == "":
                todo.append(num)
        if strict:
            for num in todo:
                report.add("SECTION_TODO_INCOMPLETE", Severity.ERROR,
                           f"§{num} ({reg.SECTION_TITLES[num]}) is TODO/empty "
                           f"(rejected under --strict)", file=path)
        else:
            report.add("STUB_REPORTED", Severity.INFO,
                       f"stub type; TODO/missing sections: {todo}", file=path)

    # --- §3 brief question set (detailed checks only for complete/strict) -
    if 3 in present and not lenient:
        body3 = rt.sections[3][1]
        cols_ok = any(
            all(c in md.normalized_header(t["header"]) for c in ("id", "source", "required", "maps_to"))
            and any("prompt" in c for c in md.normalized_header(t["header"]))
            for t in md.parse_pipe_tables(body3)
        )
        if not cols_ok:
            report.add("SECTION3_COLUMNS_BAD", Severity.ERROR,
                       "§3 table missing a required column (id, prompt, source, required, maps_to)", file=path)
        rows = rt.section3_rows()
        if rows and not any(r["required"] == "yes" for r in rows):
            sev = Severity.WARN if lenient else Severity.ERROR
            report.add("SECTION3_NO_REQUIRED_ROW", sev,
                       "§3 has no `required: yes` row (the shared validation contract)", file=path)
        seen: set = set()
        for r in rows:
            if r["source"] and r["source"] not in reg.VALID_SOURCES:
                report.add("SECTION3_SOURCE_INVALID", Severity.ERROR,
                           f"§3 `{r['id']}` source `{r['source']}` invalid", file=path)
            if r["required"] and r["required"] not in reg.VALID_REQUIRED:
                report.add("SECTION3_REQUIRED_INVALID", Severity.ERROR,
                           f"§3 `{r['id']}` required `{r['required']}` invalid", file=path)
            if r["id"] in seen or not re.fullmatch(r"[a-z0-9_]+", r["id"]):
                report.add("SECTION3_ID_BAD", Severity.WARN,
                           f"§3 id `{r['id']}` duplicated or not snake/kebab", file=path)
            seen.add(r["id"])
            if r["required"] == "yes" and not r["maps_to"]:
                report.add("REQUIRED_FIELD_NO_MAPSTO", Severity.ERROR,
                           f"required field `{r['id']}` has an empty maps_to", file=path)

    # --- templates (§6/§7) -----------------------------------------------
    if not lenient:
        ids = rt.field_ids()
        naming = rt.naming_tokens()
        for sec in (6, 7):
            if sec in present:
                for tok in sorted(set(md.snake_placeholders(rt.sections[sec][1]))):
                    if reg.classify_slot(tok, ids, naming) == "unknown":
                        report.add("TEMPLATE_SLOT_UNKNOWN_ID", Severity.ERROR,
                                   f"§{sec} template uses unknown slot `{{{tok}}}` (not a §3 field id)", file=path)
        if 6 in present and not rt.avoid_baseline_bullets():
            report.add("AVOID_TEMPLATE_EMPTY", Severity.WARN,
                       "§6 Avoid template has no literal baseline bullet", file=path)
        if 6 in present and md.has_routing_table(rt.section_body(6)):
            report.add("TEMPLATE_HAS_ROUTING", Severity.WARN,
                       "§6 CLAUDE.md template contains a routing table (belongs in CONTEXT.md)", file=path)
        if 9 in present and "DISCARD" not in rt.section_body(9):
            report.add("SECTION9_NO_DISCARD", Severity.WARN,
                       "§9 has no DISCARD row for one-off learnings", file=path)

    # --- type-table cross-check ------------------------------------------
    if known_index_types is not None and rt.name not in known_index_types:
        report.add("TYPE_TABLE_ROW_MISSING", Severity.WARN,
                   f"type `{rt.name}` has no row in the _index Type Table", file=path)


def lint_type_file(path, strict: bool = False) -> Report:
    report = Report(subcommand="lint", target=str(path))
    lint_type(reg.load_type_from_path(Path(path)), strict, report, known_index_types=None)
    return report


def lint_registry(registry_dir: Optional[str] = None, strict: bool = False,
                  types: Optional[List[str]] = None) -> Report:
    report = Report(subcommand="lint", target=str(registry_dir or reg.bundled_registry_dir()))
    index_types = reg.types_in_index(registry_dir)
    files = reg.list_type_files(registry_dir)
    file_stems = {f.stem for f in files}
    if types:
        files = [f for f in files if f.stem in types]
    for f in files:
        lint_type(reg.load_type_from_path(f), strict, report, known_index_types=index_types)
    for t in sorted(index_types - file_stems):
        report.add("TYPE_TABLE_ROW_MISSING", Severity.WARN,
                   f"Type Table lists `{t}` but registry/{t}.md does not exist")
    return report
