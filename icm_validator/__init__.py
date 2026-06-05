"""ICM structural validator — registry linter + scaffold/overlay validator.

Pure Python 3.9 standard library (no third-party deps). Two surfaces:

    python3 -m icm_validator lint [--type NAME] [--strict]
    python3 -m icm_validator validate project <dir> [--json] [--strict]

The validator is *registry-driven*: it parses the type file in `registry/` the same
way the ICM skills do (user-override-first lookup), so it never hardcodes a project
type's layout. Adding/completing a type needs no change here.

See `catalog.py` for the full list of check codes (the single source of truth shared
by the runtime, the docs, and the coverage meta-test).
"""

__version__ = "1.0.0"
SCHEMA = "icm-validate/1"
