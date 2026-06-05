"""icm-lint over the bundled registry (clean cases) + mutation matrix on a copy."""
import unittest

from icm_validator.checks_registry import lint_registry, lint_type_file
from icm_validator.findings import Severity
from tests.support import mutate as M
from tests.support.asserts import assertClean, assertFindingPresent, assertNoErrors
from tests.support.fixtures import REGISTRY, copy_to_tmp


class CleanCases(unittest.TestCase):
    def test_coding_lints_strict_clean(self):
        report = lint_registry(registry_dir=str(REGISTRY), strict=True, types=["coding"])
        assertClean(self, report)

    def test_full_bundled_registry_no_errors(self):
        report = lint_registry(registry_dir=str(REGISTRY), strict=False)
        assertNoErrors(self, report)

    def test_stubs_pass_lenient_and_are_reported(self):
        for t in ("content", "client", "business-opportunity"):
            with self.subTest(type=t):
                report = lint_registry(registry_dir=str(REGISTRY), strict=False, types=[t])
                assertNoErrors(self, report)
                assertFindingPresent(self, report, "STUB_REPORTED", Severity.INFO)

    def test_stub_under_strict_flags_todo(self):
        report = lint_registry(registry_dir=str(REGISTRY), strict=True, types=["content"])
        assertFindingPresent(self, report, "SECTION_TODO_INCOMPLETE", Severity.ERROR)


class Mutations(unittest.TestCase):
    def setUp(self):
        self.coding = copy_to_tmp(self, REGISTRY / "coding.md")

    def test_remove_section7(self):
        M.remove_numbered_section(self.coding, 7)
        assertFindingPresent(self, lint_type_file(self.coding, strict=True),
                             "SPEC_SECTION_MISSING", Severity.ERROR)

    def test_section_order(self):
        M.swap_numbered_sections(self.coding, 8, 9)
        assertFindingPresent(self, lint_type_file(self.coding, strict=True),
                             "SPEC_SECTION_ORDER", Severity.ERROR)

    def test_version_not_int(self):
        M.set_frontmatter(self.coding, "version", "four")
        assertFindingPresent(self, lint_type_file(self.coding), "FM_VERSION_NOT_INT", Severity.ERROR)

    def test_type_stem_mismatch(self):
        M.set_frontmatter(self.coding, "type", "kotding")
        assertFindingPresent(self, lint_type_file(self.coding), "FM_TYPE_STEM_MISMATCH", Severity.ERROR)

    def test_shape_invalid(self):
        M.set_frontmatter(self.coding, "shape", "banana")
        assertFindingPresent(self, lint_type_file(self.coding), "FM_SHAPE_INVALID", Severity.ERROR)

    def test_status_invalid(self):
        M.set_frontmatter(self.coding, "status", "wip")
        assertFindingPresent(self, lint_type_file(self.coding), "FM_STATUS_INVALID", Severity.ERROR)

    def test_unknown_template_slot(self):
        # inject a fresh slot into §6 that is neither a §3 id, a naming var, nor derived
        M.inject_into_numbered_section(self.coding, 6, "Bogus line with {bogus_slot} placeholder.")
        assertFindingPresent(self, lint_type_file(self.coding), "TEMPLATE_SLOT_UNKNOWN_ID", Severity.ERROR)

    def test_required_field_no_mapsto(self):
        # app_name is required: yes; blank its (ASCII) maps_to cell
        M.replace_in_file(self.coding, "project root dir name; CLAUDE.md title", "")
        assertFindingPresent(self, lint_type_file(self.coding), "REQUIRED_FIELD_NO_MAPSTO", Severity.ERROR)

    def test_frontmatter_missing(self):
        M.strip_frontmatter(self.coding)
        assertFindingPresent(self, lint_type_file(self.coding), "FM_MISSING", Severity.ERROR)

    def test_frontmatter_key_missing(self):
        M.remove_frontmatter_key(self.coding, "status")
        assertFindingPresent(self, lint_type_file(self.coding), "FM_KEY_MISSING", Severity.ERROR)

    def test_match_signals_empty(self):
        M.empty_frontmatter_list(self.coding, "match_signals")
        assertFindingPresent(self, lint_type_file(self.coding), "FM_MATCH_SIGNALS_EMPTY", Severity.WARN)

    def test_section3_columns_bad(self):
        M.replace_in_file(self.coding, "| id | prompt (plain language) | source | required | maps_to |",
                          "| id | prompt (plain language) | maps_to |")
        assertFindingPresent(self, lint_type_file(self.coding), "SECTION3_COLUMNS_BAD", Severity.ERROR)

    def test_section3_no_required_row(self):
        M.replace_in_file(self.coding, "| yes |", "| no |")
        assertFindingPresent(self, lint_type_file(self.coding), "SECTION3_NO_REQUIRED_ROW", Severity.ERROR)

    def test_section3_source_invalid(self):
        M.replace_in_file(self.coding, "user-only", "useronly")
        assertFindingPresent(self, lint_type_file(self.coding), "SECTION3_SOURCE_INVALID", Severity.ERROR)

    def test_section3_required_invalid(self):
        M.replace_in_file(self.coding, "| yes |", "| maybe |")
        assertFindingPresent(self, lint_type_file(self.coding), "SECTION3_REQUIRED_INVALID", Severity.ERROR)

    def test_section3_id_bad_duplicate(self):
        M.replace_in_file(self.coding, "| `app_name` |", "| `goal` |")
        assertFindingPresent(self, lint_type_file(self.coding), "SECTION3_ID_BAD", Severity.WARN)

    def test_avoid_template_empty(self):
        M.clear_h2_section(self.coding, "Avoid")
        assertFindingPresent(self, lint_type_file(self.coding), "AVOID_TEMPLATE_EMPTY", Severity.WARN)

    def test_template_has_routing(self):
        M.inject_into_numbered_section(
            self.coding, 6,
            "## Task Routing\n| Your Task | Go Here |\n|---|---|\n| Do X | y |\n")
        assertFindingPresent(self, lint_type_file(self.coding), "TEMPLATE_HAS_ROUTING", Severity.WARN)

    def test_section9_no_discard(self):
        M.replace_in_file(self.coding, "DISCARD", "DROPPED")
        assertFindingPresent(self, lint_type_file(self.coding), "SECTION9_NO_DISCARD", Severity.WARN)


class TypeTable(unittest.TestCase):
    def test_type_file_without_index_row(self):
        reg_dir = copy_to_tmp(self, REGISTRY)
        # a new stub type file that is NOT listed in the _index Type Table
        (reg_dir / "zzz.md").write_text(
            "---\ntype: zzz\nversion: 0\nshape: workspace\nstatus: stub\n"
            "match_signals:\n  - zzz\n---\n\n"
            "## 1. Identity\nA test stub.\n\n## 2. Match signals\nStrong: zzz.\n\n"
            "## 3. Brief question set\n\n| id | prompt | source | required | maps_to |\n"
            "|----|--------|--------|----------|---------|\n"
            "| goal | \"?\" | user-only | yes | CLAUDE.md |\n",
            encoding="utf-8",
        )
        report = lint_registry(registry_dir=str(reg_dir), strict=False)
        assertFindingPresent(self, report, "TYPE_TABLE_ROW_MISSING", Severity.WARN)


if __name__ == "__main__":
    unittest.main()
