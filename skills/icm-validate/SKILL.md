---
name: icm-validate
description: Use to QA an ICM-managed project's structure — validate the scaffold/overlay, check a clean clone, or debug why a project "doesn't feel right". Triggers on "validate my ICM project", "check the scaffold", "is this ICM structure correct", "run icm validate", "QA the structure". Runs the mechanical validator (unfilled slots, the L0/L1 split, router targets, maps_to bindings, manifest, and — brownfield — that no pre-existing file was modified) and reports findings with file:line. Read-only; never edits the project.
allowed-tools: Read, Bash
---

# icm-validate

## What this does and why
This is the **manual QA** entry point for the same mechanical validator that `project-scaffold`
runs automatically. Use it to check a project that was scaffolded elsewhere, a fresh clone, or one
that "doesn't feel right". It is **read-only** — it reports; it never edits.

The validator is *registry-driven* (it reads the project's type file), so it works for any complete
type without changes. Checks are mechanical — no LLM judgment — which is exactly why they're reliable.

## Process

### 1. Find the target
Resolve the project dir (the argument, or the current directory). Confirm it's an ICM project: it must
have `.icm/manifest.md`. If it doesn't, say so plainly ("this isn't an ICM-managed project — there's
nothing to validate") and stop.

### 2. Run the validator
```
bash "${CLAUDE_PLUGIN_ROOT}/scripts/icm" validate project "<dir>" --json
```
Also run it without `--json` to get the human-readable summary for display.

### 3. Report by exit code
- **0** — clean. Say so. (You may still surface any `info` lines, e.g. for a stub type.)
- **2** — **warnings only**: it passes, but list the warnings (e.g. a soft-default Avoid missing a
  baseline, a `maps_to` target that doesn't exist) so the user can decide.
- **1** — **errors**: list each finding with its `code` and `file:line` and a one-line plain-language
  explanation. Since this skill is read-only, **offer** to fix them (or to hand off to `project-scaffold`,
  which fixes in a loop) — don't edit here.
- **3** — `python3` is unavailable: print `${CLAUDE_PLUGIN_ROOT}/scripts/PROSE-FALLBACK-CHECKLIST.md`
  and walk the user through it manually. Note the brownfield no-touch check is weaker without python3.
- **4** — a registry/parse problem (a bug in the type file, not the project): report it as a registry
  issue, not a project failure.

### 4. Optional: `--strict`
If the user wants a pedantic pass (warnings treated as failures), add `--strict`.

## What NOT to do
- Don't edit the project — this skill only reports. Fixing is `project-scaffold`'s job (or the user's).
- Don't hand-roll the checks in prose when `python3` is available — run the real validator; it's
  deterministic and the prose path is only the fallback.
