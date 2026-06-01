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
- **Agent** — `repo-analyzer` (read-only repo inventory, used by `adopt-project`)
- **Commands** — `/icm` (overview), `/new-project`, `/adopt-project`, `/scaffold`, `/learnings`

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

## Customizing project types

Behavior per project **type** lives in one registry file bundled under the plugin
(`registry/<type>.md`). To customize or add a type **for yourself** without editing the plugin, drop
`<type>.md` into `~/.claude/icm/registry/` — it overrides the bundled default and survives plugin
updates. See `registry/MAINTAINING.md` for the full contract.

## Requirements

Claude Code with plugin support.

## License

MIT
