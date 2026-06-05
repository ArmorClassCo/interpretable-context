"""Pin the CLI contract the skills depend on: subcommands, exit codes, and --json shape.

(The python-absent prose fallback is a non-deterministic agent path, so it is not unit
tested; instead we pin the contract the fallback prose promises.)
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.support.fixtures import FIXTURES, REGISTRY, REPO_ROOT

GREEN = FIXTURES / "greenfield" / "expected-tree"


def run_module(*args):
    return subprocess.run([sys.executable, "-m", "icm_validator", *args],
                          capture_output=True, text=True, cwd=str(REPO_ROOT))


class CliContract(unittest.TestCase):
    def test_version(self):
        self.assertEqual(run_module("--version").returncode, 0)

    def test_lint_coding_strict_exit0(self):
        r = run_module("lint", "--type", "coding", "--strict", "--registry-dir", str(REGISTRY))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_validate_greenfield_exit0(self):
        r = run_module("validate", "project", str(GREEN))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_json_shape(self):
        r = run_module("validate", "project", str(GREEN), "--json")
        data = json.loads(r.stdout)
        self.assertEqual(data["schema"], "icm-validate/1")
        self.assertEqual(data["summary"]["errors"], 0)
        self.assertIn("findings", data)
        self.assertIn("exit_code", data)

    def test_errors_exit1(self):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        # empty dir -> MANIFEST_MISSING etc. (errors) -> exit 1
        self.assertEqual(run_module("validate", "project", d).returncode, 1)

    def test_usage_error_exit3(self):
        self.assertEqual(run_module("validate", "project", "/no/such/dir/xyz").returncode, 3)

    def test_no_subcommand_exit3(self):
        self.assertEqual(run_module().returncode, 3)


@unittest.skipUnless(shutil.which("bash"), "bash not available")
class Shim(unittest.TestCase):
    def test_shim_runs_validator(self):
        shim = REPO_ROOT / "scripts" / "icm"
        r = subprocess.run(["bash", str(shim), "validate", "project", str(GREEN)],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_shim_lint(self):
        shim = REPO_ROOT / "scripts" / "icm"
        r = subprocess.run(["bash", str(shim), "lint", "--type", "coding", "--strict"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
