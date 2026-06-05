"""Greenfield: the golden tree passes; each mutation is caught with the expected code."""
import unittest

from icm_validator import markdown as md, registry as reg
from icm_validator.checks_project import validate_project
from icm_validator.findings import Severity
from tests.support import mutate as M
from tests.support.asserts import assertClean, assertFindingPresent
from tests.support.fixtures import FIXTURES, REGISTRY, copy_to_tmp

GOLDEN = FIXTURES / "greenfield" / "expected-tree"


class Clean(unittest.TestCase):
    def test_golden_tree_passes(self):
        assertClean(self, validate_project(GOLDEN))

    def test_fixture_registry_version_matches_live(self):
        # drift guard: bump coding.md's version and this fails until the fixture is regenerated
        live = reg.load_type("coding", registry_dir=str(REGISTRY)).version
        manifest = md.parse_manifest((GOLDEN / ".icm/manifest.md").read_text(encoding="utf-8"))
        self.assertEqual(manifest.get("registry_version"), live,
                         f"regenerate the greenfield golden fixture for coding v{live}")


class Mutations(unittest.TestCase):
    def setUp(self):
        self.tree = copy_to_tmp(self, GOLDEN)

    def V(self):
        return validate_project(self.tree)

    def f(self, rel):
        return self.tree / rel

    # -- placeholders / bindings -----------------------------------------
    def test_slot_unresolved(self):
        M.replace_in_file(self.f("src/CONTEXT.md"), "Supabase (Postgres)", "{data_store}")
        assertFindingPresent(self, self.V(), "SLOT_UNRESOLVED", Severity.ERROR)

    def test_mapsto_value_absent(self):
        # remove the data_store needle ("Supabase") from the generated tree, both cases
        # (it is echoed lowercased in the `pick-supabase.md` ADR naming example)
        for rel in ("CLAUDE.md", "src/CONTEXT.md"):
            M.replace_in_file(self.f(rel), "Supabase", "REDACTED")
            M.replace_in_file(self.f(rel), "supabase", "redacted")
        assertFindingPresent(self, self.V(), "MAPSTO_VALUE_ABSENT", Severity.ERROR)

    def test_mapsto_target_missing(self):
        M.delete_file(self.f("ops/CONTEXT.md"))  # data_store maps_to ops/CONTEXT.md
        assertFindingPresent(self, self.V(), "MAPSTO_TARGET_MISSING", Severity.WARN)

    # -- Avoid -----------------------------------------------------------
    def test_avoid_empty(self):
        M.clear_h2_section(self.f("CLAUDE.md"), "Avoid")
        assertFindingPresent(self, self.V(), "AVOID_EMPTY", Severity.ERROR)

    def test_avoid_no_hard(self):
        M.replace_in_file(self.f("CLAUDE.md"), "### Hard constraints (never cross)", "### Other guardrails")
        assertFindingPresent(self, self.V(), "AVOID_NO_HARD", Severity.WARN)

    def test_avoid_no_baseline(self):
        M.replace_in_file(self.f("CLAUDE.md"),
                          "Don't refactor or modify areas unrelated to the current task",
                          "Tweak things freely")
        assertFindingPresent(self, self.V(), "AVOID_NO_BASELINE", Severity.WARN)

    # -- CLAUDE.md (L0) --------------------------------------------------
    def test_claude_missing(self):
        M.delete_file(self.f("CLAUDE.md"))
        assertFindingPresent(self, self.V(), "CLAUDE_MISSING", Severity.ERROR)

    def test_claude_too_long(self):
        M.append_lines(self.f("CLAUDE.md"), "\n".join(f"filler line {i}" for i in range(210)))
        assertFindingPresent(self, self.V(), "CLAUDE_TOO_LONG", Severity.ERROR)

    def test_claude_section_missing(self):
        M.replace_in_file(self.f("CLAUDE.md"), "## Current State", "## State")
        assertFindingPresent(self, self.V(), "CLAUDE_SECTION_MISSING", Severity.ERROR)

    def test_l0_has_routing_table(self):
        M.append_lines(self.f("CLAUDE.md"),
                       "## Task Routing\n| Your Task | Go Here |\n|---|---|\n| Do X | `src/CONTEXT.md` |")
        assertFindingPresent(self, self.V(), "L0_HAS_ROUTING_TABLE", Severity.ERROR)

    def test_commands_missing(self):
        M.replace_in_file(self.f("CLAUDE.md"), "## Commands", "## Cmds")
        assertFindingPresent(self, self.V(), "COMMANDS_MISSING", Severity.ERROR)

    def test_commands_empty_cell(self):
        M.replace_in_file(self.f("CLAUDE.md"), "| Install dependencies | npm install |",
                          "| Install dependencies |  |")
        assertFindingPresent(self, self.V(), "COMMANDS_EMPTY_CELL", Severity.WARN)

    # -- root CONTEXT.md (L1) -------------------------------------------
    def test_l1_missing(self):
        M.delete_file(self.f("CONTEXT.md"))
        assertFindingPresent(self, self.V(), "L1_MISSING", Severity.ERROR)

    def test_l1_not_router(self):
        # remove both the routing heading and the routing-signature table header
        M.replace_in_file(self.f("CONTEXT.md"), "## Task Routing", "## Overview")
        M.replace_in_file(self.f("CONTEXT.md"), "| Your Task | Go Here | You'll Also Need |", "| A | B | C |")
        assertFindingPresent(self, self.V(), "L1_NOT_ROUTER", Severity.ERROR)

    def test_l1_has_folder_map(self):
        M.append_lines(self.f("CONTEXT.md"), "## Folder Structure\n\nsrc/ app/ ...")
        assertFindingPresent(self, self.V(), "L1_HAS_FOLDER_MAP", Severity.ERROR)

    def test_router_target_missing(self):
        M.replace_in_file(self.f("CONTEXT.md"), "src/CONTEXT.md", "srcc/CONTEXT.md")
        assertFindingPresent(self, self.V(), "ROUTER_TARGET_MISSING", Severity.ERROR)

    # -- workspaces ------------------------------------------------------
    def test_workspace_context_missing(self):
        M.delete_file(self.f("planning/CONTEXT.md"))
        assertFindingPresent(self, self.V(), "WORKSPACE_CONTEXT_MISSING", Severity.ERROR)

    def test_workspace_empty_placeholder(self):
        M.delete_file(self.f("planning/specs/.gitkeep"))
        assertFindingPresent(self, self.V(), "WORKSPACE_EMPTY_PLACEHOLDER", Severity.WARN)

    # -- manifest --------------------------------------------------------
    def test_manifest_missing(self):
        M.delete_file(self.f(".icm/manifest.md"))
        assertFindingPresent(self, self.V(), "MANIFEST_MISSING", Severity.ERROR)

    def test_manifest_field_missing(self):
        M.remove_manifest_field(self.f(".icm/manifest.md"), "shape")
        assertFindingPresent(self, self.V(), "MANIFEST_FIELD_MISSING", Severity.ERROR)

    def test_manifest_type_unknown(self):
        M.set_manifest_field(self.f(".icm/manifest.md"), "type", "bogustype")
        assertFindingPresent(self, self.V(), "MANIFEST_TYPE_UNKNOWN", Severity.ERROR)

    def test_manifest_version_mismatch(self):
        M.set_manifest_field(self.f(".icm/manifest.md"), "registry_version", "4")
        assertFindingPresent(self, self.V(), "MANIFEST_VERSION_MISMATCH", Severity.WARN)

    def test_manifest_shape_mismatch(self):
        M.set_manifest_field(self.f(".icm/manifest.md"), "shape", "pipeline")
        assertFindingPresent(self, self.V(), "MANIFEST_SHAPE_MISMATCH", Severity.ERROR)

    def test_icm_readme_missing(self):
        M.delete_file(self.f(".icm/README.md"))
        assertFindingPresent(self, self.V(), "ICM_README_MISSING", Severity.ERROR)

    def test_icm_inbox_missing(self):
        M.delete_file(self.f(".icm/LEARNINGS-INBOX.md"))
        assertFindingPresent(self, self.V(), "ICM_INBOX_MISSING", Severity.ERROR)


if __name__ == "__main__":
    unittest.main()
