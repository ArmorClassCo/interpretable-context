---
description: Overview of the Interpretable Context (ICM) toolkit — what each skill/command does and the first-prompt-to-result flow.
---

Print the following overview to the user (adapt lightly; don't invoke other tools):

---

**Interpretable Context (ICM) toolkit** — set up and maintain AI-built projects where the folder
structure *is* the agent's architecture (a `CLAUDE.md` map → `CONTEXT.md` routers → workspace
contracts → reference vs. working layers).

**Commands**
- `/new-project [idea]` — plan a brand-new project → writes `PROJECT-BRIEF.md` (skill: `project-brief`)
- `/adopt-project [repo path]` — analyze an existing repo → writes a brownfield brief (skill: `adopt-project`)
- `/scaffold [path]` — build/overlay the ICM structure from a brief (skill: `project-scaffold`)
- `/learnings` — save this session's recurring learnings into the project (skill: `session-learnings`)

**First prompt → result**
1. **Describe an idea** (or point at a repo). `/new-project` for something new; `/adopt-project` if code already exists.
2. **Type is confirmed** (coding / content / client / business-opportunity).
3. **You answer only what you know** (goal, users, must-haves, tools you already want); the tech is **researched** (new) or **inferred from the repo** (existing).
4. **A complete `PROJECT-BRIEF.md` is written**, then it offers to scaffold.
5. **`/scaffold` builds the ICM structure** — `CLAUDE.md` (map), `CONTEXT.md` (router), per-workspace contracts, and `.icm/` markers. Brownfield overlays on top of existing code **without moving files**.
6. **You build inside the structure** — every session reads the map → router → the right workspace, no re-briefing.
7. **`/learnings` keeps it current** — when work looks done, it keeps the *recurring* learnings (a convention, a decision, a gotcha) and writes them into the project's own context files. Project-local only.

**Customize:** behavior per project *type* lives in one registry file. Bundled defaults ship with the
plugin; drop a file in `~/.claude/icm/registry/` to override or add a type without editing the plugin.

---
