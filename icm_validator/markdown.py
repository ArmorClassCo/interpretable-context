"""Small, dependency-free markdown helpers used by the checks.

No third-party YAML/Markdown libraries — just enough regex to read the ICM registry
and generated trees deterministically. The subtle bit is telling apart two kinds of
`{...}`:

  * **fillable slots** (e.g. ``{app_name}``, ``{frontend_stack}``) — substituted at
    scaffold time; an unfilled one in a generated file is a bug (SLOT_UNRESOLVED).
  * **naming-pattern variables** (e.g. ``{feature}``, ``{slug}``) — documentation that
    is *meant* to survive into the output (``planning/specs/{feature}-spec.md``).

Naming-pattern variables always appear inside inline code spans somewhere in the
templates, so :func:`inline_code_tokens` gives a registry-derived allowlist, and
:func:`snake_slots_with_lines` skips fenced blocks + inline spans for the generated-tree
scan. Both rules are registry-agnostic.
"""
from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple

# --------------------------------------------------------------------------- frontmatter

def parse_frontmatter(text: str) -> Tuple[Optional[dict], int]:
    """Parse a leading ``---`` ... ``---`` block. Returns (mapping, body_line_index).

    Supports scalars (``key: value``) and simple lists (``key:`` then ``  - item``).
    Returns (None, 0) when there is no well-formed frontmatter.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, 0
    fm: Dict[str, object] = {}
    cur_key: Optional[str] = None
    for i in range(1, len(lines)):
        line = lines[i]
        if line.strip() == "---":
            return fm, i + 1
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val == "":
                fm[key] = []
                cur_key = key
            else:
                fm[key] = val
                cur_key = None
            continue
        lm = re.match(r"^\s+-\s+(.*)$", line)
        if lm and cur_key is not None and isinstance(fm.get(cur_key), list):
            fm[cur_key].append(lm.group(1).strip())  # type: ignore[union-attr]
    return None, 0  # no closing fence


def parse_manifest(text: str) -> dict:
    """Parse an ``.icm/manifest.md`` (``key: value`` lines + optional ``workspace_map:``)."""
    data: Dict[str, object] = {}
    for line in text.splitlines():
        m = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)  # non-indented keys only
        if m and m.group(1) != "workspace_map":
            data[m.group(1)] = m.group(2).strip()

    wsmap: Dict[str, List[str]] = {}
    has_map_key = bool(re.search(r"(?m)^workspace_map:\s*$", text))
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^workspace_map:\s*$", line):
            for j in range(i + 1, len(lines)):
                ml = re.match(r"^\s+([A-Za-z0-9_./-]+):\s*(.*)$", lines[j])
                if ml:
                    wsmap[ml.group(1)] = [d.strip() for d in ml.group(2).split(",") if d.strip()]
                elif lines[j].strip() == "":
                    continue
                else:
                    break
            break
    if has_map_key or wsmap:
        data["workspace_map"] = wsmap
    return data


# --------------------------------------------------------------------------- sections

def numbered_sections(text: str) -> Tuple[Dict[int, Tuple[str, str]], List[int]]:
    """Return ({num: (title, body)}, ordered_nums) for ``## N. Title`` headings."""
    lines = text.splitlines()
    heads: List[Tuple[int, int, str]] = []
    for i, line in enumerate(lines):
        m = re.match(r"^##\s+(\d+)\.\s+(.*)$", line)
        if m:
            heads.append((i, int(m.group(1)), m.group(2).strip()))
    out: Dict[int, Tuple[str, str]] = {}
    order: List[int] = []
    for k, (i, num, title) in enumerate(heads):
        end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        out[num] = (title, "\n".join(lines[i + 1:end]))
        order.append(num)
    return out, order


def h2_titles(text: str) -> List[str]:
    """All ``## Heading`` titles (numbered or not)."""
    return [m.group(1).strip() for m in re.finditer(r"(?m)^##\s+(.+?)\s*$", text)]


def h2_section_body(text: str, title_contains: str) -> Optional[str]:
    """Body of the first ``## `` heading whose title contains ``title_contains``."""
    lines = text.splitlines()
    heads: List[Tuple[int, str]] = []
    for i, line in enumerate(lines):
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            heads.append((i, m.group(1)))
    for k, (i, title) in enumerate(heads):
        if title_contains.lower() in title.lower():
            end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
            return "\n".join(lines[i + 1:end])
    return None


# --------------------------------------------------------------------------- tables

def _split_row(line: str) -> List[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_pipe_tables(text: str) -> List[dict]:
    """Return a list of ``{"header": [...], "rows": [ {col: val}, ... ]}``."""
    tables: List[dict] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if "|" in lines[i] and i + 1 < len(lines) and "-" in lines[i + 1] and \
                re.match(r"^\s*\|?[\s:|-]+$", lines[i + 1]) and "|" in lines[i + 1]:
            header = _split_row(lines[i])
            rows: List[dict] = []
            j = i + 2
            while j < len(lines) and "|" in lines[j] and lines[j].strip():
                cells = _split_row(lines[j])
                rows.append({header[c]: (cells[c] if c < len(cells) else "") for c in range(len(header))})
                j += 1
            tables.append({"header": header, "rows": rows})
            i = j
            continue
        i += 1
    return tables


def normalized_header(header: List[str]) -> List[str]:
    return [h.strip().lower() for h in header]


# --------------------------------------------------------------------------- placeholders

def inline_code_tokens(text: str) -> set:
    """Snake ``{tokens}`` that appear inside inline code spans (the naming-var allowlist)."""
    toks: set = set()
    for span in re.findall(r"`([^`\n]+)`", text):
        toks.update(re.findall(r"\{([a-z0-9_]+)\}", span))
    return toks


def snake_placeholders(text: str) -> List[str]:
    """Every ``{snake_token}`` in the text (no skipping) — used for registry slot lint."""
    return re.findall(r"\{([a-z0-9_]+)\}", text)


def snake_slots_with_lines(text: str, skip_code: bool = True) -> List[Tuple[str, int]]:
    """``{snake}`` placeholders with 1-based line numbers.

    When ``skip_code`` (the default, for scanning *generated* files), fenced blocks and
    inline code spans are ignored so naming-pattern variables don't read as unfilled.
    """
    out: List[Tuple[str, int]] = []
    in_fence = False
    for idx, line in enumerate(text.splitlines(), start=1):
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
            continue
        if skip_code and in_fence:
            continue
        scan = re.sub(r"`[^`\n]*`", "", line) if skip_code else line
        for m in re.finditer(r"\{([a-z0-9_]+)\}", scan):
            out.append((m.group(1), idx))
    return out


# --------------------------------------------------------------------------- misc

def bullets(text: str) -> List[str]:
    """Contents of ``- `` bullet lines, excluding HTML-comment lines."""
    out: List[str] = []
    for line in text.splitlines():
        m = re.match(r"^\s*-\s+(.*)$", line)
        if m and not m.group(1).strip().startswith("<!--"):
            out.append(m.group(1).strip())
    return out


def looks_like_routing_table(header: List[str]) -> bool:
    h = normalized_header(header)
    task_col = any("task" in c for c in h)
    dest_col = any(("go here" in c or "go to" in c or "workspace" in c or "destination" in c) for c in h)
    return task_col and dest_col


def has_routing_table(text: str) -> bool:
    if any(looks_like_routing_table(t["header"]) for t in parse_pipe_tables(text)):
        return True
    return bool(re.search(r"(?im)^#+\s*task\s+routing\b", text))


def has_folder_map_or_naming(text: str) -> bool:
    return bool(re.search(r"(?im)^#+\s*(folder structure|folder map|naming conventions|naming)\b", text))


def line_count(text: str) -> int:
    return len(text.splitlines())
