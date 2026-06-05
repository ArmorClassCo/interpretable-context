# interpretable-context

A Claude Code plugin for setting up and maintaining AI-built projects using **Interpretable Context
Methodology (ICM)** — where the folder structure *is* the agent's architecture. Plan a project,
scaffold a clean ICM structure, adopt an existing repo, and capture durable learnings — so every
future session drops in with full context instead of being re-briefed each time.

It's built for people who know **what** they want to build but not necessarily the tech: it asks
only what you can answer and **researches the technical choices itself** (or, for an existing repo,
**infers them from the code**).

## What's inside

- **Skills**
  - `project-brief` — plan a NEW project → writes `PROJECT-BRIEF.md`
  - `adopt-project` — analyze an EXISTING repo → brownfield brief (with an "Existing Inventory")
  - `project-scaffold` — turn a brief into the ICM structure (or overlay it onto an existing repo)
  - `session-learnings` — capture this session's recurring learnings into the project's own files
  - `icm-validate` — QA an ICM project with the mechanical validator (read-only)
- **Agent** — `repo-analyzer` (read-only repo inventory, used by `adopt-project`)
- **Validator** — `icm_validator/` (Python 3 stdlib): `icm lint` (registry) + `icm validate project`
  (scaffold/overlay), with a golden-fixture + mutation test suite and CI
- **Commands** — `/icm` (overview), `/new-project`, `/adopt-project`, `/scaffold`, `/learnings`, `/icm-validate`

## Install

### From GitHub
```
/plugin marketplace add ArmorClassCo/interpretable-context
/plugin install interpretable-context@icm
```
or with the CLI:
```
claude plugin marketplace add https://github.com/ArmorClassCo/interpretable-context.git
claude plugin install interpretable-context@icm
```

### From a local folder
```
claude plugin marketplace add /path/to/interpretable-context
claude plugin install interpretable-context@icm
```

Then **restart Claude Code / open a new session** to activate it. Run `/icm` for a guided overview.

## Quick start

1. **New idea →** `/new-project` (or just describe it). **Existing repo →** `/adopt-project`.
2. It confirms the project **type**, asks only what you know, and researches/infers the tech.
3. It writes `PROJECT-BRIEF.md`, then **`/scaffold`** builds the ICM structure — greenfield, or a
   brownfield *overlay* on your repo (**no existing files are moved**).
4. Build inside the structure. When a chunk of work looks done, **`/learnings`** saves the *recurring*
   conventions/decisions/gotchas into the project's own context files (project-local only).

## How it works (ICM layers)

- **L0 `CLAUDE.md`** — the always-loaded map (identity, folder tree, commands, guardrails)
- **L1 `CONTEXT.md`** — the router (task → workspace)
- **L2 per-workspace `CONTEXT.md`** — the contract for each workspace
- **L3** — stable, recurring reference material · **L4** — per-run working artifacts

Keeping the map (L0) and router (L1) separate keeps the always-loaded context tiny.

## Validation (QA on the scaffold)

A scaffold is only useful if it's *correct*. `project-scaffold` runs a **mechanical validator** in a
generate → validate → fix loop, and you can run it yourself any time with **`/icm-validate`** (or
`bash scripts/icm validate project <dir>`). It checks — deterministically, no LLM judgment — that:

- no `{slot}` placeholders are left unfilled;
- the **L0/L1 split** holds (no routing table in `CLAUDE.md`, no folder map in the root `CONTEXT.md`);
- every router target resolves and every workspace has a contract;
- every required brief field's value actually **landed** in the structure (the `maps_to` binding);
- the `.icm/manifest.md` is well-formed; and
- for a **brownfield overlay**, that **no pre-existing file was modified, moved, or deleted**
  (re-hashed against an `.icm/baseline.json` snapshot).

The validator is **registry-driven** — it reads the project's type file, so it works for any type
without changes. It's pure Python 3 standard library (no `pip`); if `python3` is absent the skills
fall back to a prose checklist. Run `bash scripts/icm lint` to check the registry itself.

## Customizing project types

Behavior per project **type** lives in one registry file bundled under the plugin
(`registry/<type>.md`). To customize or add a type **for yourself** without editing the plugin, drop
`<type>.md` into `~/.claude/icm/registry/` — it overrides the bundled default and survives plugin
updates. See `registry/MAINTAINING.md` for the full contract.

## Requirements

Claude Code with plugin support. The validator uses **Python 3** (standard library only — no `pip`);
it's optional — without it the skills fall back to a prose validation checklist.

## License

MIT
