---
name: adopt-project
description: Use when there is an EXISTING repo or codebase to bring under ICM structure — not a brand-new idea. Triggers on "I have an existing project/repo", "adopt this codebase", "add structure to my existing app", "I'm improving an existing website/app", "generate a brief from this repo", "set up ICM on top of this". Analyzes the repo, infers the tech itself, and writes a PROJECT-BRIEF.md (with an Existing Inventory) that project-scaffold overlays onto the code without moving any files. Use this instead of project-brief whenever code already exists.
allowed-tools: Read, Glob, Grep, Bash, Agent, AskUserQuestion, Write
---

# adopt-project

## What this produces and why

This is the **brownfield** counterpart to `project-brief`. Instead of interviewing someone about a
new idea, it **analyzes an existing repository** and writes the same `PROJECT-BRIEF.md` — plus an
**"Existing Inventory"** that maps the repo's current folders onto ICM layers. `project-scaffold`
then lays the ICM context/routing layer *on top of* the code **without moving or rewriting a single
file**, so future sessions get the ICM benefits (a map, routers, workspace contracts) over work that
already exists.

It does the technical reading so the user doesn't have to: the stack, data store, and tooling are
**inferred from the repo**, not asked.

## The registry is the source of truth

**Registry location & lookup order.** The registry ships in this plugin at
`${CLAUDE_PLUGIN_ROOT}/registry/`. For any registry file, use `~/.claude/icm/registry/<file>` if it
exists (user override), otherwise `${CLAUDE_PLUGIN_ROOT}/registry/<file>` (bundled default).

- `<registry>/_index.md` — Type Table (classify) + format spec.
- `<registry>/<type>.md` — the type's §3 "Brief question set" **and** §10 "Existing-repo mapping".

## Process

### 1. Locate the repo
Identify the repo root (an argument, or the current directory). Confirm it in one line:
*"I'll analyze `<path>` and set up ICM structure on top of it — right?"* If there's clearly no code
there (empty dir, just an idea), this is the wrong skill — point the user to `project-brief`.

### 2. Classify the type — and ALWAYS confirm
Read `_index.md`'s Type Table; match the repo (its README, languages, layout) against `match signals`.
Most code repos are `coding`. Confirm in one line; if only weak signals, present options. If the
matched type is a `stub`, say the mapping will be minimal and offer to treat it as `coding`.

### 3. Load the type's question set + mapping
Read the type's registry file: its **§3** question set (so you know what the brief must contain) and
its **§10** existing-repo mapping (how to read the stack and map dirs → ICM layers).

### 4. Inventory the repo with the `repo-analyzer` agent
Dispatch the **`repo-analyzer`** agent (use the `Agent` tool, `subagent_type: repo-analyzer`). Pass
it the repo path **and the §10 mapping table** so it applies the right rules. For a large repo you
may run two scoped analyzers in parallel (e.g. one for app code, one for infra/docs) and merge. The
agent returns: detected stack (with evidence), a directory map, a proposed `dir → ICM layer` mapping,
and brief signals. It writes nothing.

### 5. Fill the brief — infer first, then ask only the gaps
- **Auto-fill the `researchable` §3 fields** (`frontend_stack`, `backend_stack`, `data_store`,
  `auth`, `hosting`, `package_manager`) from the analyzer's evidence. Don't web-search what the repo
  already tells you. Only research a researchable field if the repo truly doesn't reveal it.
- **Ask the user ONLY the `user-only` intent gaps** the repo can't answer: `goal` and `users` (unless
  the README states them clearly — then confirm rather than ask), any **planned** `known_tools`
  they intend to add, and `constraints` / `things_to_avoid`. **Avoid matters even more for brownfield**
  — it protects what already works. Propose guardrails drawn from the repo and confirm them: e.g.
  "don't modify the existing deploy workflow / Dockerfile", "don't break the public API in `src/…`",
  "don't touch the legacy `{module}`", plus the usual scope/stack/secrets ones. Don't leave Avoid empty.

### 5.5. Coverage re-read pass
Re-scan **both** the repo-analyzer output **and** the conversation for facts that aren't yet captured —
a CLI/entrypoint mentioned in the README, a deploy quirk, a "do not touch" the user said in passing,
an existing ADR worth seeding. Map each to a field, an Avoid (HARD if it protects something that
works), or the Existing Inventory before validating. Brownfield loses context most easily here.

### 6. Validation pass
Check every `required: yes` field is filled (inferred or answered). If a required field is still
`UNKNOWN`, ask or research it before writing. This is the same zero-missing-context contract
`project-scaffold` re-checks.

### 7. Write `PROJECT-BRIEF.md` at the repo root
Same format as `project-brief`, plus an **Existing Inventory** section and `origin: brownfield`:

```markdown
# Project Brief: {app_name}

- **Type:** {type}
- **Origin:** brownfield (adopted from existing repo)
- **Created:** {date}

## Identity
- Goal: {goal}
- Users: {users}
- Platform: {platform}

## Structure Manifest
<!-- one entry per answered/inferred §3 field, by id, tagged with provenance:
     [user] | [user-confirmed-default] | [inferred-from-repo] -->
- {id}: {answer}  [{provenance}]
- ...

## Existing Inventory
<!-- from repo-analyzer; the proposed mapping project-scaffold will overlay. Flag for confirmation.
     This table IS the source for the manifest's `workspace_map:` (workspace -> existing dirs). -->
| Existing path | Maps to (ICM workspace / layer) | Notes |
|---------------|----------------------------------|-------|
| `src/` | src/ (L4 app code) | entry: src/index.ts |
| `docs/` | docs/ (L3/L4) | |
| ... | ... | |
- Workspaces to ADD (absent in repo): {e.g. planning/}
- Directories left as-is (no workspace): {list}

## Things to Avoid
### Hard (never cross)
- {brownfield guardrails that protect what works: "don't modify the Dockerfile/deploy workflow",
  "don't break the public API in `src/…`", "don't touch the legacy `{module}`", + secrets}
### Soft (revisitable defaults)
- {researched/assumed defaults the user didn't hard-require}

## Reference Material to Seed (L3)
- {existing ADRs/specs/architecture docs worth seeding; "none" if nothing}

## Provenance
- User-provided: {ids}
- Inferred from repo: {ids, each with the file evidence}
- Researched: {ids, with one-line rationale} (usually none for brownfield)
```

The **Existing Inventory** "Maps to" column is what `project-scaffold` turns into the manifest's
`workspace_map:` block, which `icm validate` uses to prove the overlay points only at real existing
dirs and touched no source file.

### 8. Offer the next step
Tell the user the brief is written, and offer: *"Want me to overlay the ICM structure now (no files
will be moved)?"* If yes, that's `project-scaffold` (it detects `origin: brownfield` and runs overlay
mode). Don't auto-run it.

## Idempotency
If `PROJECT-BRIEF.md` already exists at the repo root, read it, show what's there, and ask before
overwriting.

## What NOT to do
- **Never modify, move, rename, or delete any existing file** — you only read the repo and write the
  brief.
- Don't ask the user technical questions the repo already answers — infer those.
- Don't scaffold folders — that's `project-scaffold`. Don't skip type confirmation or leave required
  fields empty.
