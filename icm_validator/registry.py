"""Registry loader/parser. Everything the validator knows about a project *type* is
derived from its registry file here — so the validator stays registry-driven and a new
or completed type needs no validator change.
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Dict, List, Optional

from . import markdown as md

# The 10 FORMAT-SPEC sections (registry/_index.md).
SECTION_TITLES = {
    1: "Identity",
    2: "Match signals",
    3: "Brief question set",
    4: "Folder tree",
    5: "Layer map",
    6: "CLAUDE.md template",
    7: "CONTEXT.md templates",
    8: "Naming conventions",
    9: "Learning-routing rules",
    10: "Existing-repo mapping",
}
COMPLETE_REQUIRED = set(range(1, 11))       # complete types need all ten
STUB_REQUIRED = {1, 2, 3}                    # stubs need at least these
VALID_SHAPES = {"workspace", "pipeline"}
VALID_STATUS = {"complete", "stub"}
VALID_SOURCES = {"user-only", "researchable"}
VALID_REQUIRED = {"yes", "no"}

# Controlled provenance vocabulary (mirrored in registry/_index.md).
PROVENANCE_VOCAB = {
    "user", "user-confirmed-default", "assumed-default", "inferred-from-repo", "learned",
    "scaffold-baseline", "researched",
}


class RegistryError(Exception):
    pass


def type_file_path(name: str, override_dir: Optional[str] = None) -> Path:
    """User-override-first resolution of a single type file (mirrors the skills)."""
    fname = f"{name}.md"
    if override_dir:
        return Path(override_dir) / fname
    user = Path.home() / ".claude" / "icm" / "registry" / fname
    if user.exists():
        return user
    env = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env and (Path(env) / "registry" / fname).exists():
        return Path(env) / "registry" / fname
    return Path(__file__).resolve().parent.parent / "registry" / fname


def bundled_registry_dir() -> Path:
    env = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env and (Path(env) / "registry").is_dir():
        return Path(env) / "registry"
    return Path(__file__).resolve().parent.parent / "registry"


def list_type_files(registry_dir: Optional[str] = None) -> List[Path]:
    d = Path(registry_dir) if registry_dir else bundled_registry_dir()
    return sorted(p for p in d.glob("*.md") if p.stem not in {"_index", "MAINTAINING"})


def types_in_index(registry_dir: Optional[str] = None) -> set:
    d = Path(registry_dir) if registry_dir else bundled_registry_dir()
    idx = d / "_index.md"
    if not idx.exists():
        return set()
    names: set = set()
    for t in md.parse_pipe_tables(idx.read_text(encoding="utf-8")):
        if md.normalized_header(t["header"])[:1] == ["type"]:
            for row in t["rows"]:
                first = next(iter(row.values()), "")
                m = re.search(r"`([a-z0-9-]+)`", first)
                if m:
                    names.add(m.group(1))
    return names


def classify_slot(token: str, ids: set, naming_tokens: set) -> str:
    """direct | naming | derived | unknown — for a pure-snake template ``{token}``."""
    if token in ids:
        return "direct"
    if token in naming_tokens:
        return "naming"
    if re.search(r"(_cmd$|_date$|_from_|_inline|_install|_tree_|_without_)", token):
        return "derived"
    return "unknown"


class RegistryType:
    def __init__(self, name: str, path: Path, text: str):
        self.name = name
        self.path = path
        self.text = text
        self.frontmatter, _ = md.parse_frontmatter(text)
        self.sections, self.order = md.numbered_sections(text)

    # -- frontmatter -------------------------------------------------------
    @property
    def status(self) -> str:
        return str((self.frontmatter or {}).get("status", "")).strip()

    @property
    def shape(self) -> str:
        return str((self.frontmatter or {}).get("shape", "")).strip()

    @property
    def version(self) -> str:
        return str((self.frontmatter or {}).get("version", "")).strip()

    @property
    def is_stub(self) -> bool:
        return self.status == "stub"

    # -- section 3 (brief question set) -----------------------------------
    def section3_rows(self) -> List[dict]:
        if 3 not in self.sections:
            return []
        body = self.sections[3][1]
        for t in md.parse_pipe_tables(body):
            hdr = md.normalized_header(t["header"])
            if "id" in hdr and "source" in hdr and "required" in hdr and "maps_to" in hdr:
                raw = t["header"]
                idx = {c: raw[hdr.index(c)] for c in ("id", "source", "required", "maps_to")}
                prompt_raw = next((raw[i] for i, h in enumerate(hdr) if "prompt" in h), None)
                rows = []
                for r in t["rows"]:
                    rows.append({
                        "id": r.get(idx["id"], "").strip().strip("`"),
                        "prompt": r.get(prompt_raw, "").strip() if prompt_raw else "",
                        "source": r.get(idx["source"], "").strip().strip("`"),
                        "required": r.get(idx["required"], "").strip().strip("`").lower(),
                        "maps_to": r.get(idx["maps_to"], "").strip(),
                    })
                return [r for r in rows if r["id"]]
        return []

    def required_fields(self) -> List[dict]:
        return [r for r in self.section3_rows() if r["required"] == "yes"]

    # -- templates ---------------------------------------------------------
    def section_body(self, num: int) -> str:
        return self.sections.get(num, ("", ""))[1]

    def naming_tokens(self) -> set:
        return md.inline_code_tokens(self.text)

    def field_ids(self) -> set:
        return {r["id"] for r in self.section3_rows()}

    def claude_headings(self) -> List[str]:
        """The ``## `` headings the §6 CLAUDE.md template defines (required in output)."""
        return md.h2_titles(self.section_body(6))

    def avoid_baseline_bullets(self) -> List[str]:
        """Baseline guardrail bullets in the §6 template's Avoid section.

        A baseline is a real prose bullet (it may embed slots like ``{hosting}``); the
        ``{each thing_to_avoid …}`` instruction lines are not bullets, so they're skipped.
        """
        body = md.h2_section_body(self.section_body(6), "Avoid")
        if body is None:
            return []
        out = []
        for b in md.bullets(body):
            residual = re.sub(r"\{[^}]*\}", "", b).strip()
            if len(residual) >= 12:
                out.append(b)
        return out

    def workspace_dirs(self) -> List[str]:
        """Workspace directories (L2) from the §5 Layer map."""
        for t in md.parse_pipe_tables(self.section_body(5)):
            for row in t["rows"]:
                cells = list(row.values())
                if cells and re.search(r"\bL2\b", cells[0]):
                    return sorted(set(re.findall(r"([A-Za-z0-9_]+)/CONTEXT\.md", cells[-1])))
        return []


def load_type(name: str, registry_dir: Optional[str] = None) -> RegistryType:
    path = type_file_path(name, registry_dir)
    if not path.exists():
        raise RegistryError(f"registry type file not found: {path}")
    return RegistryType(name, path, path.read_text(encoding="utf-8"))


def load_type_from_path(path: Path) -> RegistryType:
    return RegistryType(path.stem, path, path.read_text(encoding="utf-8"))
