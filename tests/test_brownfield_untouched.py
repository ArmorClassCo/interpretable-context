"""The brownfield "no source file touched" invariant, proven three independent ways:
an in-test hash oracle, an only-ICM-files-added check, and the validator agreeing.
"""
import unittest
from pathlib import Path

from icm_validator import baseline as bl
from icm_validator.checks_project import validate_project
from icm_validator.findings import Severity
from tests.support import mutate as M
from tests.support.asserts import assertFindingPresent, assertNoCode
from tests.support.fixtures import FIXTURES, copy_to_tmp

EXISTING = FIXTURES / "brownfield" / "existing-repo"
OVERLAY = FIXTURES / "brownfield" / "expected-overlay"
PROTECTED = ["package.json", "next.config.js", "Dockerfile",
             "src/app/page.tsx", "src/lib/db.ts", "docs/architecture/data-model.md"]
ICM_TOP = {"CLAUDE.md", "CONTEXT.md", "PROJECT-BRIEF.md", ".icm", "planning", "ops"}


def _hashes(root, rels):
    return {r: bl.sha256_file(Path(root) / r) for r in rels}


class Untouched(unittest.TestCase):
    def test_protected_files_byte_identical(self):
        self.assertEqual(_hashes(EXISTING, PROTECTED), _hashes(OVERLAY, PROTECTED),
                         "the overlay must not alter any pre-existing file")

    def test_overlay_only_adds_icm_files(self):
        existing = {p.relative_to(EXISTING).as_posix() for p in EXISTING.rglob("*") if p.is_file()}
        overlay = {p.relative_to(OVERLAY).as_posix() for p in OVERLAY.rglob("*") if p.is_file()}
        for rel in overlay - existing:
            top = rel.split("/")[0]
            self.assertIn(top, ICM_TOP | {"src", "docs"}, f"unexpected added file: {rel}")
            if top in ("src", "docs"):
                self.assertTrue(rel.endswith("/CONTEXT.md"),
                                f"only a CONTEXT.md may be added under existing {top}/: {rel}")

    def test_validator_agrees_untouched(self):
        r = validate_project(copy_to_tmp(self, OVERLAY))
        assertNoCode(self, r, "BROWNFIELD_SOURCE_MODIFIED")
        assertNoCode(self, r, "BROWNFIELD_SOURCE_DELETED")

    def test_independent_oracle_and_validator_catch_tamper(self):
        tree = copy_to_tmp(self, OVERLAY)
        M.replace_in_file(tree / "src/app/page.tsx", "Notesy", "TAMPERED")
        # (a) independent in-test hash oracle
        self.assertNotEqual(bl.sha256_file(EXISTING / "src/app/page.tsx"),
                            bl.sha256_file(tree / "src/app/page.tsx"))
        # (b) the validator agrees
        assertFindingPresent(self, validate_project(tree), "BROWNFIELD_SOURCE_MODIFIED", Severity.ERROR)


if __name__ == "__main__":
    unittest.main()
