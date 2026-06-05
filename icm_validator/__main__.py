"""Command-line interface:

    python3 -m icm_validator lint     [--type N ...] [--registry-dir DIR] [--strict] [--json]
    python3 -m icm_validator validate project <dir> [--registry-dir DIR] [--strict] [--json]

Exit codes (the calling skills branch on these): 0 clean · 1 errors · 2 warnings-only ·
3 usage error · 4 registry/parse failure.
"""
import argparse
import os
import sys

from . import __version__
from .checks_project import validate_project
from .checks_registry import lint_registry
from .findings import EXIT_USAGE


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="icm", description="ICM structural validator (registry-driven)")
    p.add_argument("--version", action="version", version=f"icm-validator {__version__}")
    sub = p.add_subparsers(dest="cmd")

    pl = sub.add_parser("lint", help="lint registry type files against the FORMAT SPEC")
    pl.add_argument("--type", action="append", dest="types", metavar="NAME",
                    help="limit to a type (repeatable)")
    pl.add_argument("--registry-dir", dest="registry_dir")
    pl.add_argument("--strict", action="store_true")
    pl.add_argument("--json", action="store_true")

    pv = sub.add_parser("validate", help="validate a scaffolded/overlaid ICM project")
    pv.add_argument("kind", choices=["project"])
    pv.add_argument("path")
    pv.add_argument("--registry-dir", dest="registry_dir")
    pv.add_argument("--strict", action="store_true")
    pv.add_argument("--json", action="store_true")
    return p


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    parser = build_parser()
    args = parser.parse_args(argv)

    strict = getattr(args, "strict", False)
    if args.cmd == "lint":
        report = lint_registry(registry_dir=args.registry_dir, strict=strict, types=args.types)
    elif args.cmd == "validate":
        if not os.path.isdir(args.path):
            print(f"icm: not a directory: {args.path}", file=sys.stderr)
            return EXIT_USAGE
        report = validate_project(args.path, registry_dir=args.registry_dir)
    else:
        parser.print_help(sys.stderr)
        return EXIT_USAGE

    print(report.to_json(strict=strict) if args.json else report.human(strict=strict))
    return report.exit_code(strict=strict)


if __name__ == "__main__":
    sys.exit(main())
