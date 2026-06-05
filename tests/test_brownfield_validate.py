"""Brownfield: the golden overlay passes; each overlay-invariant mutation is caught.

Fixtures are validated from a TEMP COPY (outside any git repo) so the git cross-check is
correctly skipped and mutations never touch the committed fixture.
"""
import shutil
import subprocess
import unittest

from icm_validator import markdown as md, registry as reg
from icm_validator.checks_project import validate_project
from icm_validator.findings import Severity
from tests.support import mutate as M
from tests.support.asserts import assertClean, assertFindingPresent
from tests.support.fixtures import FIXTURES, REGISTRY, copy_to_tmp

OVERLAY = FIXTURES / "brownfield" / "expected-overlay"


class Clean(unittest.TestCase):
    def test_overlay_passes(self):
        tree = copy_to_tmp(self, OVERLAY)
        assertClean(self, validate_project(tree))

    def test_fixture_registry_version_matches_live(self):
        live = reg.load_type("coding", registry_dir=str(REGISTRY)).version
        manifest = md.parse_manifest((OVERLAY / ".icm/manifest.md").read_text(encoding="utf-8"))
        self.assertEqual(manifest.get("registry_version"), live,
                         f"regenerate the brownfield golden fixture for coding v{live}")


class Mutations(unittest.TestCase):
    def setUp(self):
        self.tree = copy_to_tmp(self, OVERLAY)

    def V(self):
        return validate_project(self.tree)

    def f(self, rel):
        return self.tree / rel

    def test_source_modified(self):
        M.replace_in_file(self.f("src/app/page.tsx"), "Notesy", "Notesy!!")
        assertFindingPresent(self, self.V(), "BROWNFIELD_SOURCE_MODIFIED", Severity.ERROR)

    def test_source_deleted(self):
        M.delete_file(self.f("src/lib/db.ts"))
        assertFindingPresent(self, self.V(), "BROWNFIELD_SOURCE_DELETED", Severity.ERROR)

    def test_source_moved(self):
        content = M.read(self.f("src/lib/db.ts"))
        M.delete_file(self.f("src/lib/db.ts"))
        M.write_file(self.f("src/lib/db2.ts"), content)
        r = self.V()
        assertFindingPresent(self, r, "BROWNFIELD_SOURCE_DELETED", Severity.ERROR)
        assertFindingPresent(self, r, "BROWNFIELD_UNTRACKED_NONICM", Severity.ERROR)

    def test_nonicm_added(self):
        M.write_file(self.f("src/app/extra.tsx"), "export const x = 1;\n")
        assertFindingPresent(self, self.V(), "BROWNFIELD_UNTRACKED_NONICM", Severity.ERROR)

    def test_empty_placeholder(self):
        M.touch_dir(self.f("ops/deploy"))
        assertFindingPresent(self, self.V(), "OVERLAY_EMPTY_PLACEHOLDER", Severity.WARN)

    def test_baseline_missing(self):
        M.delete_file(self.f(".icm/baseline.json"))
        assertFindingPresent(self, self.V(), "BASELINE_MISSING", Severity.ERROR)

    def test_baseline_unparseable(self):
        M.write_file(self.f(".icm/baseline.json"), "not json {")
        assertFindingPresent(self, self.V(), "BASELINE_UNPARSEABLE", Severity.ERROR)

    def test_workspace_map_missing(self):
        M.write(self.f(".icm/manifest.md"), M.read(self.f(".icm/manifest.md")).split("workspace_map:")[0])
        assertFindingPresent(self, self.V(), "WORKSPACE_MAP_MISSING", Severity.ERROR)

    def test_workspace_dir_unmapped(self):
        M.replace_in_file(self.f(".icm/manifest.md"), "  src: src/app, src/lib", "  src:")
        assertFindingPresent(self, self.V(), "WORKSPACE_DIR_UNMAPPED", Severity.ERROR)

    def test_workspace_dir_nonexistent(self):
        M.replace_in_file(self.f(".icm/manifest.md"), "  src: src/app, src/lib", "  src: src/legacy")
        assertFindingPresent(self, self.V(), "WORKSPACE_DIR_NONEXISTENT", Severity.ERROR)


@unittest.skipUnless(shutil.which("git"), "git not available")
class GitCrossCheck(unittest.TestCase):
    def test_git_tracked_modified(self):
        tree = copy_to_tmp(self, OVERLAY)
        subprocess.run(["git", "init", "-q", str(tree)], check=True)
        subprocess.run(["git", "-C", str(tree), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(tree), "-c", "user.email=t@t", "-c", "user.name=t",
                        "commit", "-q", "-m", "init"], check=True)
        M.replace_in_file(tree / "src/app/page.tsx", "Notesy", "Notesy!!")
        assertFindingPresent(self, validate_project(tree), "GIT_TRACKED_MODIFIED", Severity.WARN)


if __name__ == "__main__":
    unittest.main()
