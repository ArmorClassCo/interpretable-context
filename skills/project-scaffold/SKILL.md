---
name: project-scaffold
description: Use when a PROJECT-BRIEF.md exists and the project's folders and routing files need
  to be created — i.e. building or scaffolding a project's structure, workspace layout, or ICM
  file tree. Triggers on "build the structure", "scaffold this project", "set up the folders",
  "create the workspace", or right after project-brief finishes. Reads the brief, loads the
  matching type from the shared registry, and generates the CLAUDE.md map, CONTEXT.md routers,
  workspace contracts, and .icm/ marker files. Use this rather than hand-rolling folders so the
  structure matches how project-brief and session-learnings expect it.
allowed-tools: Read, Write, Bash
---

# project-scaffold

## What this does and why

This skill turns a `PROJECT-BRIEF.md` into a complete **ICM** folder + routing structure. ICM
(Interpretable Context Methodology) makes the folder structure itself the agent's architecture, so
that any future session can drop into the project, read the right files, and work without being
re-briefed every time.

It builds the structure from the **shared registry**, not from improvisation, so the layout stays
consistent with what `project-brief` collected and what `session-learnings` will later maintain.
All three skills read the same registry — that's what keeps them in sync.

## The five layers (what you're building)

- **L0 `CLAUDE.md`** — THE MAP. Always loaded, so it must stay lean (< 200 lines): identity, folder
  tree, naming, commands, what to avoid, current state. **No routing tables here.**
- **L1 root `CONTEXT.md`** — THE ROUTER. Loaded when navigating: task → workspace table, workspace
  summary, cross-workspace flow. **No folder map or naming here.**
- **L2 per-workspace `CONTEXT.md`** — the contract for that workspace (what it's for, what to load
  and skip, its process, its skills, what not to do).
- **L3** — stable reference material that recurs across work (architecture, decisions, conventions).
- **L4** — per-run working artifacts (code, specs, generated docs).

Keeping L0 and L1 in **separate files** is the core token-management move: the always-loaded map
stays tiny, and routing detail is paid for only when you actually navigate.

## Process

### 1. Read the brief → get the type
Read the project's `PROJECT-BRIEF.md`. Take the declared `type` and the Structure Manifest (the
field-by-field answers). Note the **origin**: a brief with an **"Existing Inventory"** section (or
`origin: brownfield` in its provenance) means you're laying ICM *on top of* an existing codebase —
see "Overlay mode" (§4b). Otherwise it's a greenfield build.

### 2. Load the type's registry entry
Read the type's registry file. **Registry location & lookup order:** the registry ships at
`${CLAUDE_PLUGIN_ROOT}/registry/`; for any registry file use `~/.claude/icm/registry/<file>` if it
exists (user override), otherwise `${CLAUDE_PLUGIN_ROOT}/registry/<file>` (bundled default). You'll use:
- §4 Folder tree, §5 Layer map → what to create
- §6 CLAUDE.md template, §7 CONTEXT.md templates → what to generate
- §8 Naming conventions
- the file's frontmatter `version` → to stamp into the manifest

If the type is a `stub` (sections marked TODO), tell the user the structure will be minimal and
build what the stub does define (at least L0/L1 + `.icm/`), rather than inventing a full layout.

### 3. Re-validate the brief
Check the brief has every `required: yes` field from the type's §3 question set. **If any is
missing, STOP** — don't build a partial structure. Tell the user which fields are missing and point
them back to `project-brief`. (Both skills validate against the same `required` rows; see the
registry's `MAINTAINING.md`.)

### 4. Create the folder tree
Create the directories from the registry's §4 tree, filling `{slots}` (like `{app_name}`) from the
brief's manifest. Notes:
- **Scaffold into the existing project directory** the brief lives in. Don't rename that directory
  to `{app_name}` — use `{app_name}` only for titles and file *content*. (The folder may be
  `toolshare/` while the app is "ToolShare"; that's fine.)
- Create L4 working directories empty, but drop a `.gitkeep` file in each otherwise-empty directory
  so the tree survives `git add`/clone (empty dirs aren't tracked by git).
- Create any **leaf files** shown in the §4 tree that aren't generated below — e.g.
  `docs/changelog.md` with a `# Changelog` header.

### 4b. Overlay mode (brownfield projects)
If the brief is brownfield (step 1), you are **adding the ICM context/routing layer over an existing
repo — never reshaping it**:
- **Snapshot the repo FIRST — before creating any ICM file.** Write `.icm/baseline.json`, a record of
  every pre-existing file's path + sha256 + size (plus the ICM `tool_paths` you're about to add). This
  is what lets `icm validate` later prove the overlay modified nothing. If `python3` is present, use the
  helper: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/icm_baseline.py" "<repo>" {YYYY-MM-DD} > "<repo>/.icm/baseline.json"`
  (create `.icm/` first). Write it **once**: on a re-scaffold of an already-adopted repo, do NOT
  regenerate it — it must keep reflecting the original pre-ICM state.
- **Do not create, move, rename, or modify any existing source.** Read the brief's "Existing
  Inventory" (discovered dirs → proposed ICM layer, per the type's §10 mapping).
- Add only what's missing: the L0/L1 files, `.icm/`, per-workspace `CONTEXT.md` placed at the
  existing workspace roots, and any genuinely-absent workspace (e.g. add `planning/` if there's no
  planning home). Point each `CONTEXT.md` at the dirs that already exist rather than inventing new ones.
- The generated `CLAUDE.md` (§6) **describes where things already are**; the routers (§7) point at the
  existing dirs as-is. `.gitkeep` only newly-created empty dirs. Then continue to §5 and §6.
- **No empty placeholders in overlay mode.** Create a workspace dir only to hold its `CONTEXT.md`
  contract (pointing at the real existing locations); do NOT create empty L4 subdirs (`ops/deploy/`,
  `docs/api/`, …) that don't correspond to anything actually in the repo. Multiple existing code dirs
  (e.g. `src/` + `app/`) map to the single `src/` workspace — record them in the manifest's dir-map.

### 5. Generate the files
- **Root `CLAUDE.md`** from §6 — fill the slots; keep it map-only and under 200 lines; **do not add
  a routing table**. Keep the "Maintenance" footer that reminds the agent to offer `session-learnings`
  at task completion — that footer is the hook-free trigger for Skill 3. **Emit Avoid as the type's
  §6 template defines it — HARD constraints + SOFT defaults — and never empty.** The brief's HARD
  `things_to_avoid` / `constraints` render under `### Hard constraints`; the secrets baseline also
  goes there. Researched/assumed defaults and the rest of the baseline floor (scope / off-stack tech /
  unrelated refactors) render under `### Soft defaults`, each carrying `— default, {created_date},
  provenance: {scaffold-baseline|assumed-default}`. (This hard/soft split is the ARA §7.4 lesson: a
  capable future session must be able to tell a real limit from a revisitable default.) If the brief
  carries no specifics, emit the baselines anyway and note the brief looks underspecified.
- **Root `CONTEXT.md`** from §7a — router only; **no folder map or naming**.
- **Each workspace/stage `CONTEXT.md`** from §7b onward — fill from the brief. Two rules for the
  capability sections:
  - **Skills & Tools is the type's curated baseline — emit every baseline row even if a skill
    isn't installed in this session** (the install-link footnote ships with the table, so any
    future session can fix that). Do NOT silently drop or swap baseline rows; the registry owns
    the baseline. Resolve the `{plus one row per … known_tools …}` instruction: each brief
    `known_tools` entry gets a row in the most relevant workspace's table (naming its MCP/CLI if
    one exists); if there are none, just remove the instruction line.
  - **Known Gotchas** starts as the template ships it ("None recorded yet.") — it is
    session-learnings' append target, not something to pre-fill at scaffold time.
- **Seed L3 reference** — if the brief lists reference material, drop it into the appropriate L3
  location (e.g. `planning/architecture/`).
- **`.icm/manifest.md`**:
  ```
  # ICM Manifest
  type: {type}
  registry_version: {version from the registry file's frontmatter}
  shape: {workspace|pipeline}
  origin: {greenfield|brownfield}
  created: {YYYY-MM-DD}
  ```
  For **brownfield** projects, append a `workspace_map:` block — one indented `workspace: dir1, dir2`
  line per workspace, pointing at the real existing directories it covers — so both `icm validate`
  (overlay invariants) and `session-learnings` route to the project's actual folders:
  ```
  workspace_map:
    src: src/app, src/lib
    ops: Dockerfile
    planning: docs/architecture
  ```
  This is also how `session-learnings` later identifies the project, its type, and its layout. If the
  registry file has no `version`, record `registry_version: unknown` and note it.
- **`.icm/LEARNINGS-INBOX.md`** — create empty with a one-line header.
- **`.icm/README.md`** — one line: "This folder marks an ICM-managed project. See manifest.md."

### 6. Report
Show the created tree and suggest next steps (start planning a feature, etc.). For brownfield
overlays, report **what was added vs. what was left untouched** so it's clear no existing code moved.
Do **not** build any application code — that's out of scope; you're building the structure that makes
building easier.

**Recommended-skills check (prompt, never block).** Compare each skill named in the generated
Skills & Tools tables against the skills actually available in this session. For any that are
missing, tell the user plainly — *"This structure expects `superpowers:systematic-debugging`,
which isn't installed — install superpowers from https://github.com/obra/superpowers (the link is
also in the generated file)"* — using the install links from the type file's §7 footnotes. The
rows stay in the generated files either way (they become live as soon as the user installs), and
a missing skill is never a reason to stop, re-generate, or fail validation.

### 7. Validate the scaffold (generate → validate → fix)
Before declaring success, run the bundled validator and fix what it flags:
```
bash "${CLAUDE_PLUGIN_ROOT}/scripts/icm" validate project "<project-dir>" --json
```
Branch on the exit code:
- **0** — clean. **2** — warnings only: surface them, but it passes.
- **1** — one or more **errors**: read the findings (each carries a `code` + `file`:`line`), fix the
  named files, and **re-run**. Repeat at most **3 rounds**, then stop and show the user any remaining
  findings rather than looping forever.
- **3** — `python3` is unavailable: fall back to `${CLAUDE_PLUGIN_ROOT}/scripts/PROSE-FALLBACK-CHECKLIST.md`
  and self-verify against it (note: the prose path cannot re-hash files, so the brownfield no-touch
  guarantee is weaker — recommend installing `python3` for brownfield).
- **4** — a registry/parse problem (a bug in the type file, not this project): stop and tell the user; don't retry.

The checks are mechanical — unfilled `{slots}`, the L0/L1 split (no routing table in `CLAUDE.md`),
every router target resolves, every required field's value actually landed in the tree, the manifest
is well-formed, and (brownfield) **no pre-existing file was modified**. Passing them is what turns a
structurally-complete scaffold into a *verified* one.

## Idempotency
If part of the tree already exists, don't clobber it. Compare against the template and **ask before
overwriting** any file that already has content. **Never overwrite L4 working directories** (`src/`,
`specs/`, generated docs) — those hold real work. **Never regenerate `.icm/baseline.json`** on a
re-scaffold — it is the record of what predated ICM, and rewriting it would hide a later violation.

## What NOT to do
- Don't put routing tables in `CLAUDE.md`, or folder maps in the root `CONTEXT.md` — the split is
  the point.
- Don't proceed if `required` fields are missing — send the user back to `project-brief`.
- Don't write application code or invent structure the registry doesn't define.
