# ICM scaffold validation — prose fallback checklist

Use this **only when `python3` is unavailable** (the `scripts/icm` shim exited 3). It restates the
validator's **error-severity** checks in plain language so an agent can self-verify by reading the
generated files. The real validator (`icm validate project`) is deterministic and preferred; this
prose path cannot re-hash files, so the brownfield "no file touched" guarantee is **weaker** here —
install `python3` for brownfield work.

Read each generated file and confirm:

## `.icm/`
- [ ] `.icm/manifest.md` exists and has `type`, `registry_version`, `shape`, `origin`, `created`.
- [ ] `.icm/README.md` and `.icm/LEARNINGS-INBOX.md` exist.
- [ ] The `type` names a real registry type file.

## No unfilled slots
- [ ] **No `{slot}` placeholders remain** in any generated file (CLAUDE.md, every CONTEXT.md,
      `.icm/*.md`). Naming-pattern variables that live inside `` `backticks` `` or ``` ``` ``` code
      fences (e.g. `` `planning/specs/{feature}-spec.md` ``) are meant to stay — everything else must
      be filled.

## `CLAUDE.md` (L0 = the map)
- [ ] Under 200 lines.
- [ ] Has the sections the type's §6 template defines (typically: What This Is, Folder Structure,
      Naming Conventions, Commands, Avoid, Current State, Maintenance).
- [ ] **Contains NO routing table** (no "Task Routing" / "Go Here" table — routing lives in CONTEXT.md).
- [ ] **Avoid is non-empty** and split into `### Hard constraints` + `### Soft defaults`; the type's
      baseline guardrails are present; soft defaults carry a date + provenance.
- [ ] The Commands table has no `{slot}` (literal `TBD` is fine).

## Root `CONTEXT.md` (L1 = the router)
- [ ] Has a task → workspace routing table.
- [ ] Contains **no folder map and no naming rules** (those live in CLAUDE.md).
- [ ] Every routing target (e.g. `planning/CONTEXT.md`) resolves to a file/dir that exists.

## Workspaces & bindings
- [ ] Every workspace directory has its own `CONTEXT.md`.
- [ ] Every `required: yes` field from the brief actually appears where the templates place it
      (e.g. the stack values in `src/CONTEXT.md`, the app name in the CLAUDE.md title).

## Brownfield overlay only
- [ ] **No pre-existing file was modified, moved, or deleted** (compare against your memory of the
      repo before you started — and strongly prefer running the real validator, which re-hashes
      `.icm/baseline.json`).
- [ ] Only ICM files were added (CLAUDE.md, CONTEXT.md, `*/CONTEXT.md`, `.icm/**`, the new workspace
      dirs). No empty placeholder directories were created.
- [ ] The manifest's `workspace_map:` points at real existing directories.

If anything fails, fix the named file and re-check. Stop after 3 rounds and surface what remains.
