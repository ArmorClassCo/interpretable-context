"""Paths to the repo + helpers to copy a committed fixture into a temp dir for mutation."""
import shutil
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
REGISTRY = REPO_ROOT / "registry"
FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def copy_to_tmp(testcase, src):
    """Copy a file or directory into a fresh temp dir; auto-cleanup; return the temp copy."""
    src = Path(src)
    tmp = Path(tempfile.mkdtemp(prefix="icm-"))
    testcase.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
    dest = tmp / src.name
    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)
    return dest
