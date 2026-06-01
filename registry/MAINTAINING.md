# Maintaining the ICM Skills System

The skills + shared registry ship as the **`interpretable-context` plugin**. This file is the
contract that keeps them in sync. Read it before changing any of them.

**Customization surface = the registry, not the skills/commands/agent.** Change a type's behavior by
editing its registry file (the bundled copy, or a `~/.claude/icm/registry/` override). The skills,
the `repo-analyzer` agent, and the commands are generic machinery — you rarely touch them.

## The pieces

| Piece | Location | Role |
|-------|----------|------|
| Shared registry | `${CLAUDE_PLUGIN_ROOT}/registry/*.md` (bundled); `~/.claude/icm/registry/*.md` (user override, checked first) | Single source of truth, one file per project type |
| `project-brief` | plugin `skills/project-brief/` | Classifies a new project, gathers/researches its brief |
| `adopt-project` | plugin `skills/adopt-project/` | Analyzes an existing repo → brief (brownfield) |
| `project-scaffold` | plugin `skills/project-scaffold/` | Builds the folder/routing structure (greenfield or brownfield overlay) |
| `session-learnings` | plugin `skills/session-learnings/` | Captures recurring learnings into a project's files |
| `repo-analyzer` (agent) | plugin `agents/` | Read-only repo inventory used by `adopt-project` |
| Commands | plugin `commands/` | Thin entry points: `/icm`, `/new-project`, `/adopt-project`, `/scaffold`, `/learnings` |

## The golden rule

**Edit the registry, not the skills, to change a type's behavior.** Each type file
(`registry/<type>.md`) co-locates everything the three skills need for that type, so changing a
type's structure forces you to update its questions and its learning-routing right beside it —
they cannot drift. The skills are generic engines; the registry is the data they run on.

## Registry section → consumer mapping

(Full FORMAT SPEC lives in `_index.md`, beside this file.)

| Section | Read by |
|---------|---------|
| Frontmatter (`type`, `version`, `shape`, `match_signals`, `status`) | all skills |
| §1 Identity, §2 Match signals | project-brief **and** adopt-project (classify) |
| §3 Brief question set | project-brief & adopt-project (ask/infer) **and** project-scaffold (re-validate) |
| §4 Folder tree, §5 Layer map | project-scaffold (build) **and** session-learnings (route) |
| §6 CLAUDE.md template, §7 CONTEXT.md templates | project-scaffold (generate) |
| §8 Naming conventions | project-scaffold **and** session-learnings |
| §9 Learning-routing rules | session-learnings (file learnings) |
| §10 Existing-repo mapping | adopt-project (inventory) **and** project-scaffold (overlay) |

## The shared validation contract

The `required: yes` rows in a type's §3 question set are the **single definition** of "a complete
brief." Both `project-brief` (final validation pass) and `project-scaffold` (re-validation before
building) check against those same rows. If you add/remove a required field, you change both
skills' behavior at once — by design.

## Skill 3 invariant (project-local)

`session-learnings` writes **only inside the current project** — its `.icm/` directory and its own
structure files (`CLAUDE.md`, `*/CONTEXT.md`, new ADRs). It **never** modifies the skills, the
bundled or user-override registry, or any global config. Future projects are unaffected by what it
does in one project.

## Promoting a learning to the registry (the only path to future projects — manual)

If a learning earned in one project should apply to *all* future projects of a type:
1. Open the type's registry file — the bundled `${CLAUDE_PLUGIN_ROOT}/registry/<type>.md` to change
   it for everyone, or `~/.claude/icm/registry/<type>.md` to override it just for yourself.
2. Add it to the appropriate section — e.g. a new convention into the §7 `src/CONTEXT.md`
   template's "Patterns We Follow", or a default into the §6 `CLAUDE.md` template, or a new §3
   question, or a new §9 routing rule.
3. Bump the file's `version`.
This is a deliberate human action. No skill ever does it automatically.

## Adding a new project type

See the "Adding a new type" checklist in `_index.md`. In short: copy a file, fill the 10 sections,
add a Type Table row, set `status: complete` + `version: 1`. No skill code changes. (To add it just
for yourself, drop the file in `~/.claude/icm/registry/`.)

## Keeping the skills and registry aligned when you edit one

- Changed a **type's folder shape** (§4/§5)? → check §7 templates and §9 routing still match.
- Added a **required question** (§3)? → both skills enforce it automatically; make sure §4/§6/§7
  actually use the new field (its `maps_to`).
- Changed a **skill's process**? → if it changed what it reads from the registry, update the
  FORMAT SPEC in `_index.md` and every type file, or the skill will read fields that don't exist.
