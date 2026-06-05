"""1-line mutation primitives operating on a copied fixture tree or file.

Always operate on a *copy* (see fixtures.copy_to_tmp) — never the committed fixture.
"""
import re
from pathlib import Path


def read(path):
    return Path(path).read_text(encoding="utf-8")


def write(path, text):
    Path(path).write_text(text, encoding="utf-8")


def replace_in_file(path, old, new):
    write(path, read(path).replace(old, new))


def append_lines(path, text):
    write(path, read(path) + "\n" + text + "\n")


def delete_file(path):
    Path(path).unlink()


def write_file(path, content=""):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def touch_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def set_frontmatter(path, key, value):
    text = read(path)
    new, n = re.subn(rf"(?m)^({re.escape(key)}):[ \t]*.*$", rf"\g<1>: {value}", text, count=1)
    if n == 0:
        new = re.sub(r"^---\n", f"---\n{key}: {value}\n", text, count=1)
    write(path, new)


def remove_numbered_section(path, num):
    """Delete a ``## N. ...`` section (only numbered headings are boundaries)."""
    out, skipping = [], False
    for line in read(path).splitlines():
        m = re.match(r"^##\s+(\d+)\.", line)
        if m:
            skipping = int(m.group(1)) == num
        if not skipping:
            out.append(line)
    write(path, "\n".join(out) + "\n")


def inject_into_numbered_section(path, num, text):
    """Append ``text`` at the end of section ``## num.`` (before the next numbered heading)."""
    out, in_sec, injected = [], False, False
    for line in read(path).splitlines():
        m = re.match(r"^##\s+(\d+)\.", line)
        if m and in_sec and not injected:
            out.append(text)
            injected = True
        if m:
            in_sec = int(m.group(1)) == num
        out.append(line)
    if in_sec and not injected:
        out.append(text)
    write(path, "\n".join(out) + "\n")


def swap_numbered_sections(path, a, b):
    """Swap the numeric labels of two ``## N.`` headings (creates an out-of-order file)."""
    text = read(path)
    text = re.sub(rf"(?m)^(##\s+){a}\.", rf"\g<1>{a}_TMP.", text, count=1)
    text = re.sub(rf"(?m)^(##\s+){b}\.", rf"\g<1>{a}.", text, count=1)
    text = re.sub(rf"(?m)^(##\s+){a}_TMP\.", rf"\g<1>{b}.", text, count=1)
    write(path, text)


def clear_h2_section(path, title):
    """Keep the ``## title`` heading but remove its body (down to the next ``## ``)."""
    out, in_sec = [], False
    for line in read(path).splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            in_sec = title.lower() in m.group(1).lower()
            out.append(line)
            continue
        if in_sec:
            continue
        out.append(line)
    write(path, "\n".join(out) + "\n")


def set_manifest_field(path, key, value):
    """Set a ``key: value`` line in an .icm/manifest.md (insert if absent)."""
    text = read(path)
    new, n = re.subn(rf"(?m)^({re.escape(key)}):[ \t]*.*$", rf"\g<1>: {value}", text, count=1)
    if n == 0:
        new = text.rstrip("\n") + f"\n{key}: {value}\n"
    write(path, new)


def remove_manifest_field(path, key):
    text = read(path)
    write(path, re.sub(rf"(?m)^{re.escape(key)}:.*$\n?", "", text))


def strip_frontmatter(path):
    """Remove a leading ``---`` … ``---`` block entirely."""
    text = read(path)
    write(path, re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S))


def remove_frontmatter_key(path, key):
    """Delete a scalar ``key: value`` line from the frontmatter."""
    write(path, re.sub(rf"(?m)^{re.escape(key)}:.*$\n?", "", read(path), count=1))


def empty_frontmatter_list(path, key):
    """Drop the ``- item`` lines under a frontmatter ``key:`` list (leaves it empty)."""
    out, in_list = [], False
    for line in read(path).splitlines():
        if re.match(rf"^{re.escape(key)}:\s*$", line):
            out.append(line)
            in_list = True
            continue
        if in_list:
            if re.match(r"^\s+-\s+", line):
                continue
            in_list = False
        out.append(line)
    write(path, "\n".join(out) + "\n")
