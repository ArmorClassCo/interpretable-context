"""Meta-test: every error/warn check code in the catalog is exercised by at least one
test (a failing mutation). INFO codes and documented COVERAGE_EXEMPT codes are skipped.

This makes the test suite track the validator — adding a new check code without a test
fails CI.
"""
import unittest
from pathlib import Path

from icm_validator.catalog import CATALOG, COVERAGE_EXEMPT
from icm_validator.findings import Severity
from tests.support.fixtures import REPO_ROOT

TESTS_DIR = REPO_ROOT / "tests"


def _all_test_source() -> str:
    parts = []
    for f in sorted(TESTS_DIR.glob("test_*.py")):
        if f.name != "test_coverage_manifest.py":
            parts.append(f.read_text(encoding="utf-8"))
    return "\n".join(parts)


class CoverageManifest(unittest.TestCase):
    def test_every_error_and_warn_code_is_tested(self):
        src = _all_test_source()
        missing = []
        for code, (sev, _applies, _title) in CATALOG.items():
            if sev == Severity.INFO or code in COVERAGE_EXEMPT:
                continue
            if f'"{code}"' not in src:
                missing.append(code)
        self.assertFalse(missing, f"catalog codes with no failing-mutation test: {missing}")

    def test_exempt_codes_are_real(self):
        for code in COVERAGE_EXEMPT:
            self.assertIn(code, CATALOG, f"COVERAGE_EXEMPT lists unknown code {code}")

    def test_info_codes_have_a_pass_reference(self):
        # INFO codes should still be referenced somewhere (a pass assertion), e.g. STUB_REPORTED
        src = _all_test_source()
        for code, (sev, _a, _t) in CATALOG.items():
            if sev == Severity.INFO:
                self.assertIn(f'"{code}"', src, f"INFO code {code} is never referenced in tests")


if __name__ == "__main__":
    unittest.main()
