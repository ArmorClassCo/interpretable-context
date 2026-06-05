"""The validator's output model: Finding, Severity, Report, and exit codes."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Sequence


class Severity(str, Enum):
    ERROR = "error"
    WARN = "warn"
    INFO = "info"


# Exit codes the calling skills branch on (documented in the SKILL contract).
EXIT_OK = 0          # clean (no errors; warnings allowed)
EXIT_ERRORS = 1      # >=1 error finding -> the generate/validate/fix loop must retry
EXIT_WARNINGS = 2    # warnings only and not --strict -> pass, but surface them
EXIT_USAGE = 3       # validator usage error (bad args / missing target) -> prose fallback
EXIT_REGISTRY = 4    # registry/parse failure -> "registry bug", do not retry the project


@dataclass
class Finding:
    code: str
    severity: Severity
    message: str
    file: Optional[str] = None
    line: Optional[int] = None
    hint: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "severity": self.severity.value,
            "file": self.file,
            "line": self.line,
            "message": self.message,
            "hint": self.hint,
        }


@dataclass
class Report:
    subcommand: str
    target: Optional[str] = None
    origin: Optional[str] = None
    findings: List[Finding] = field(default_factory=list)
    registry_failure: bool = False  # set when a parse failure makes checking unreliable

    # -- collection --------------------------------------------------------
    def add(
        self,
        code: str,
        severity: Severity,
        message: str,
        file: Optional[str] = None,
        line: Optional[int] = None,
        hint: Optional[str] = None,
    ) -> None:
        self.findings.append(Finding(code, severity, message, file, line, hint))

    def extend(self, findings: Sequence[Finding]) -> None:
        self.findings.extend(findings)

    # -- views -------------------------------------------------------------
    def by_severity(self, sev: Severity) -> List[Finding]:
        return [f for f in self.findings if f.severity == sev]

    @property
    def errors(self) -> List[Finding]:
        return self.by_severity(Severity.ERROR)

    @property
    def warnings(self) -> List[Finding]:
        return self.by_severity(Severity.WARN)

    @property
    def infos(self) -> List[Finding]:
        return self.by_severity(Severity.INFO)

    def codes(self) -> List[str]:
        return [f.code for f in self.findings]

    def has(self, code: str) -> bool:
        return any(f.code == code for f in self.findings)

    # -- output ------------------------------------------------------------
    def exit_code(self, strict: bool = False) -> int:
        if self.registry_failure:
            return EXIT_REGISTRY
        if self.errors:
            return EXIT_ERRORS
        if self.warnings:
            return EXIT_ERRORS if strict else EXIT_WARNINGS
        return EXIT_OK

    def to_json(self, strict: bool = False) -> str:
        return json.dumps(
            {
                "schema": "icm-validate/1",
                "subcommand": self.subcommand,
                "target": self.target,
                "origin": self.origin,
                "summary": {
                    "errors": len(self.errors),
                    "warnings": len(self.warnings),
                    "infos": len(self.infos),
                },
                "exit_code": self.exit_code(strict),
                "findings": [f.to_dict() for f in self.findings],
            },
            indent=2,
        )

    def human(self, strict: bool = False) -> str:
        label = {Severity.ERROR: "ERROR", Severity.WARN: "WARN ", Severity.INFO: "INFO "}
        lines: List[str] = []
        for sev in (Severity.ERROR, Severity.WARN, Severity.INFO):
            for f in self.by_severity(sev):
                loc = f.file or ""
                if f.line:
                    loc += f":{f.line}"
                loc = f"{loc}  " if loc else ""
                lines.append(f"{label[sev]} {f.code}  {loc}{f.message}")
                if f.hint:
                    lines.append(f"           - {f.hint}")
        lines.append("")
        verdict = "PASS" if self.exit_code(strict) in (EXIT_OK, EXIT_WARNINGS) else "FAIL"
        lines.append(
            f"{verdict}: {len(self.errors)} error(s), "
            f"{len(self.warnings)} warning(s), {len(self.infos)} info"
        )
        return "\n".join(lines)
