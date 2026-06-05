"""Assertion helpers shared by the validator tests."""
from icm_validator.findings import Severity


def codes(report):
    return [f.code for f in report.findings]


def assertFindingPresent(tc, report, code, severity=None):
    matches = [f for f in report.findings if f.code == code]
    tc.assertTrue(matches, f"expected finding {code}; got {codes(report)}")
    if severity is not None:
        tc.assertTrue(
            any(f.severity == severity for f in matches),
            f"{code} present but not at severity {severity.value}",
        )


def assertNoCode(tc, report, code):
    tc.assertNotIn(code, codes(report), f"unexpected finding {code}: {codes(report)}")


def assertClean(tc, report):
    """No error or warn findings (info allowed)."""
    bad = [(f.code, f.severity.value) for f in report.findings
           if f.severity in (Severity.ERROR, Severity.WARN)]
    tc.assertFalse(bad, f"expected clean; got {bad}")


def assertNoErrors(tc, report):
    tc.assertFalse(report.errors, f"expected no errors; got {[f.code for f in report.errors]}")
