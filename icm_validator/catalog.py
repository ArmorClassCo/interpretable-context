"""The check catalog as data — the single source of truth for every check code.

Each entry maps a stable CODE -> (default Severity, applies_to, title).

`applies_to` is a tuple drawn from:
    "registry"    -- emitted by `icm lint` over a registry type file
    "greenfield"  -- emitted by `icm validate project` on a from-scratch scaffold
    "brownfield"  -- emitted by `icm validate project` on an overlaid existing repo

The runtime, the docs in registry/_index.md, and tests/test_coverage_manifest.py all
read THIS table, so the catalog can never drift from the implementation. The coverage
meta-test asserts every non-INFO code here has at least one pass test and one failing
mutation (except codes listed in COVERAGE_EXEMPT, with a documented reason).
"""
from .findings import Severity as S

# code -> (severity, applies_to, title)
CATALOG = {
    # ------------------------------------------------------------------ registry lint
    "FM_MISSING": (S.ERROR, ("registry",), "Frontmatter missing or unparseable"),
    "FM_KEY_MISSING": (S.ERROR, ("registry",), "Required frontmatter key missing"),
    "FM_TYPE_STEM_MISMATCH": (S.ERROR, ("registry",), "frontmatter `type` != filename stem"),
    "FM_VERSION_NOT_INT": (S.ERROR, ("registry",), "frontmatter `version` is not an integer"),
    "FM_SHAPE_INVALID": (S.ERROR, ("registry",), "`shape` not in {workspace, pipeline}"),
    "FM_STATUS_INVALID": (S.ERROR, ("registry",), "`status` not in {complete, stub}"),
    "FM_MATCH_SIGNALS_EMPTY": (S.WARN, ("registry",), "`match_signals` is empty"),
    "SPEC_SECTION_MISSING": (S.ERROR, ("registry",), "A required FORMAT-SPEC section is missing"),
    "SPEC_SECTION_ORDER": (S.ERROR, ("registry",), "Sections are out of the required 1..10 order"),
    "SECTION_TODO_INCOMPLETE": (S.ERROR, ("registry",), "Section is TODO/empty (rejected under --strict)"),
    "SECTION3_COLUMNS_BAD": (S.ERROR, ("registry",), "§3 table is missing a required column"),
    "SECTION3_NO_REQUIRED_ROW": (S.ERROR, ("registry",), "§3 has no `required: yes` row"),
    "SECTION3_SOURCE_INVALID": (S.ERROR, ("registry",), "§3 `source` cell invalid"),
    "SECTION3_REQUIRED_INVALID": (S.ERROR, ("registry",), "§3 `required` cell invalid"),
    "SECTION3_ID_BAD": (S.WARN, ("registry",), "§3 `id` duplicated or not kebab/snake"),
    "TEMPLATE_SLOT_UNKNOWN_ID": (S.ERROR, ("registry",), "A {slot} in a §6/§7 template is not a known field id"),
    "REQUIRED_FIELD_NO_MAPSTO": (S.ERROR, ("registry",), "A `required: yes` field has an empty `maps_to`"),
    "AVOID_TEMPLATE_EMPTY": (S.WARN, ("registry",), "§6 Avoid template has no literal baseline bullet"),
    "TEMPLATE_HAS_ROUTING": (S.WARN, ("registry",), "§6 CLAUDE.md template contains a routing table"),
    "SECTION9_NO_DISCARD": (S.WARN, ("registry",), "§9 learning-routing has no DISCARD row"),
    "STUB_REPORTED": (S.INFO, ("registry",), "Type is a stub; some sections are intentionally TODO"),
    "TYPE_TABLE_ROW_MISSING": (S.WARN, ("registry",), "Type file has no row in the _index Type Table (or vice-versa)"),

    # ------------------------------------------------------------- project (shared G,B)
    "MANIFEST_MISSING": (S.ERROR, ("greenfield", "brownfield"), ".icm/manifest.md is missing"),
    "MANIFEST_FIELD_MISSING": (S.ERROR, ("greenfield", "brownfield"), ".icm/manifest.md is missing a required key"),
    "MANIFEST_TYPE_UNKNOWN": (S.ERROR, ("greenfield", "brownfield"), "manifest `type` has no registry file"),
    "MANIFEST_VERSION_MISMATCH": (S.WARN, ("greenfield", "brownfield"), "manifest `registry_version` != live registry version"),
    "MANIFEST_SHAPE_MISMATCH": (S.ERROR, ("greenfield", "brownfield"), "manifest `shape` != registry `shape`"),
    "ICM_README_MISSING": (S.ERROR, ("greenfield", "brownfield"), ".icm/README.md is missing"),
    "ICM_INBOX_MISSING": (S.ERROR, ("greenfield", "brownfield"), ".icm/LEARNINGS-INBOX.md is missing"),
    "SLOT_UNRESOLVED": (S.ERROR, ("greenfield", "brownfield"), "An unfilled {slot} placeholder remains in a generated file"),
    "CLAUDE_MISSING": (S.ERROR, ("greenfield", "brownfield"), "CLAUDE.md is missing"),
    "CLAUDE_TOO_LONG": (S.ERROR, ("greenfield", "brownfield"), "CLAUDE.md is >= 200 lines (L0 must stay lean)"),
    "CLAUDE_SECTION_MISSING": (S.ERROR, ("greenfield", "brownfield"), "CLAUDE.md is missing a required L0 section"),
    "L0_HAS_ROUTING_TABLE": (S.ERROR, ("greenfield", "brownfield"), "CLAUDE.md contains a routing table (belongs in CONTEXT.md)"),
    "AVOID_EMPTY": (S.ERROR, ("greenfield", "brownfield"), "CLAUDE.md Avoid section is empty"),
    "AVOID_NO_HARD": (S.WARN, ("greenfield", "brownfield"), "CLAUDE.md Avoid lacks a Hard-constraints subsection"),
    "AVOID_NO_BASELINE": (S.WARN, ("greenfield", "brownfield"), "CLAUDE.md Avoid is missing the type's baseline guardrails"),
    "COMMANDS_MISSING": (S.ERROR, ("greenfield", "brownfield"), "CLAUDE.md has no Commands table"),
    "COMMANDS_EMPTY_CELL": (S.WARN, ("greenfield", "brownfield"), "A Commands table row has an empty command cell"),
    "L1_MISSING": (S.ERROR, ("greenfield", "brownfield"), "Root CONTEXT.md is missing"),
    "L1_NOT_ROUTER": (S.ERROR, ("greenfield", "brownfield"), "Root CONTEXT.md has no task->workspace routing table"),
    "L1_HAS_FOLDER_MAP": (S.ERROR, ("greenfield", "brownfield"), "Root CONTEXT.md contains a folder map / naming (belongs in CLAUDE.md)"),
    "ROUTER_TARGET_MISSING": (S.ERROR, ("greenfield", "brownfield"), "A routing-table target does not resolve to an existing path"),
    "WORKSPACE_CONTEXT_MISSING": (S.ERROR, ("greenfield", "brownfield"), "A workspace directory has no CONTEXT.md"),
    "MAPSTO_VALUE_ABSENT": (S.ERROR, ("greenfield", "brownfield"), "A required field's value is absent where its maps_to places it"),
    "MAPSTO_TARGET_MISSING": (S.WARN, ("greenfield", "brownfield"), "A field's maps_to target file does not exist"),

    # ----------------------------------------------------------- project (greenfield)
    "WORKSPACE_EMPTY_PLACEHOLDER": (S.WARN, ("greenfield",), "An empty L4 dir has no .gitkeep (won't survive git)"),

    # ----------------------------------------------------------- project (brownfield)
    "BASELINE_MISSING": (S.ERROR, ("brownfield",), ".icm/baseline.json is missing (overlay must write it first)"),
    "BASELINE_UNPARSEABLE": (S.ERROR, ("brownfield",), ".icm/baseline.json is not valid JSON / wrong shape"),
    "BROWNFIELD_SOURCE_MODIFIED": (S.ERROR, ("brownfield",), "A pre-existing file was modified by the overlay"),
    "BROWNFIELD_SOURCE_DELETED": (S.ERROR, ("brownfield",), "A pre-existing file was moved or deleted by the overlay"),
    "BROWNFIELD_UNTRACKED_NONICM": (S.ERROR, ("brownfield",), "The overlay added a non-ICM file"),
    "OVERLAY_EMPTY_PLACEHOLDER": (S.WARN, ("brownfield",), "The overlay created an empty placeholder directory"),
    "WORKSPACE_MAP_MISSING": (S.ERROR, ("brownfield",), "Brownfield manifest has no workspace_map block"),
    "WORKSPACE_DIR_UNMAPPED": (S.ERROR, ("brownfield",), "A workspace has a CONTEXT.md but no existing-dir mapping"),
    "WORKSPACE_DIR_NONEXISTENT": (S.ERROR, ("brownfield",), "A workspace_map entry points at a non-existent directory"),
    "GIT_TRACKED_MODIFIED": (S.WARN, ("brownfield",), "git reports a non-ICM tracked file as modified/deleted/renamed"),
}


def severity_of(code: str) -> S:
    return CATALOG[code][0]


def applies_to(code: str):
    return CATALOG[code][1]


# Codes the coverage meta-test does not require a dedicated failing mutation for.
# Keep this list tiny and documented; INFO codes are exempt automatically.
COVERAGE_EXEMPT = {
    # Exercised only when a real git work-tree is present; covered by an opt-in git
    # test when git is available, but exempt so the suite stays green without git.
    "GIT_TRACKED_MODIFIED": "requires a git work-tree; covered by test_brownfield git path when git is present",
}
