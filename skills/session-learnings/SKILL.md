---
name: session-learnings
description: Use when work in an ICM-managed project (one that has a .icm/manifest.md) looks finished and reusable learnings might be worth saving — new conventions, gotchas, decisions, commands, things to avoid — or on explicit request like "extract learnings", "update the project's CLAUDE.md from what we did", "save what we learned", "capture learnings", "what should we remember from this session". Offers to scan the session, keeps only the learnings that will recur, and updates the project's own context files with the user's approval. Never edits the skills, the registry, or global config.
allowed-tools: Read, Write, Edit, AskUserQuestion, Bash
---

# session-learnings

## What this does and why

Over a working session, a project earns small pieces of durable knowledge — a convention the team
settled on, a gotcha that wasted an hour, a decision, a command that works. If those evaporate when
the session ends, the next session relearns them the hard way. This skill captures them **into the
project's own context files** so the structure stays current and self-documenting.

The key discipline is **separating what recurs from what doesn't.** A convention you'll follow in
all future code is worth saving (it's "the factory" — ICM Layer 3). A one-off ("renamed this file
once") is not (it's "the product" — Layer 4, and it's already done). Saving one-offs just bloats the
context everyone loads every time. So this skill keeps only the recurring learnings and discards the
rest.

## When to use it

- **Offered at task completion:** when a chunk of work in an ICM project looks done, offer it:
  *"Want me to check this session for anything worth saving to the project — conventions, gotchas,
  decisions?"* (The scaffolded project's `CLAUDE.md` has a Maintenance note reminding you to offer.)
- **On request, anytime:** "extract learnings", "update the project context", "save what we learned".

This is in-session and interactive — you reason over the conversation you're already in, propose
what's worth keeping, and apply it once the user approves. There is no hook and no background job.

## Precondition

The current project must be ICM-managed — i.e. `.icm/manifest.md` exists at the project root. If it
doesn't, say so plainly ("this isn't an ICM-managed project, so there's nowhere structured to file
learnings") and stop. Don't invent structure.

## Invariant — this is project-local only

Write **only inside the current project**: its `.icm/` directory and its own structure files
(`CLAUDE.md`, the workspace `CONTEXT.md` files, new ADRs under `planning/decisions/`). **Never**
modify the skills themselves, the plugin's bundled registry (`${CLAUDE_PLUGIN_ROOT}/registry/`), the
user-override registry (`~/.claude/icm/registry/`), or any global config. Future projects must be
unaffected by what you do here. (If a learning genuinely should apply to all future projects of this
type, tell the user that's a manual registry edit — see the registry's `MAINTAINING.md` — and don't
do it automatically.)

## Process

### 1. Identify the project and load its routing rules
Read `.icm/manifest.md` → get `type` (and, if present, `origin` and the `workspace → existing-dir`
map). Read the type's registry file and use its §9 "Learning-routing rules" (where each kind of
learning goes, and the recurrence test) and §5 "Layer map" (what's L3 vs L4). Read only that one type file.

**Registry location & lookup order:** use `~/.claude/icm/registry/<type>.md` if it exists (user
override), otherwise `${CLAUDE_PLUGIN_ROOT}/registry/<type>.md` (bundled default).

For a **brownfield** project, the manifest's `workspace → existing-dir` map tells you the real
destination directories — route learnings to those actual folders rather than the default tree paths.

### 2. Pass 1 — capture candidates
Look back over what happened in this session and gather candidate learnings, each tagged with a
category from §9 (typically: new-convention, thing-to-avoid, current-state-update, gotcha, decision,
command, dependency-stale). Good signals:
- a mistake hit more than once, then a fix that worked (→ thing-to-avoid or gotcha)
- the user correcting you ("no, do it this way") (→ convention)
- a decision the user settled (→ decision)
- a command that turned out to be the right one (→ command)
- a persistent state change ("we switched to Postgres") (→ current-state-update)

### 3. Pass 2 — the recurrence test (this is the important filter)
For each candidate ask: **does this touch something that will recur or be referenced again?**
- **Yes →** keep it (it belongs in the factory / Layer 3).
- **No, it was a one-off →** discard it. Don't stage it anywhere.
Be honest here — most of what happens in a session is one-off. **Zero survivors is a perfectly valid
outcome**; if nothing recurs, say "nothing this session is worth saving permanently" and stop.

### 4. Route and format the survivors
For each survivor, use §9 to determine the destination file + section and the exact insert format.
Prepare, for each: the learning, its category, the destination (file → section), the exact text to
insert, and a one-line recurrence justification.

### 5. Present for approval
Show the user the proposed learnings as a clean list (you may also write this list into
`.icm/LEARNINGS-INBOX.md` so there's a record). For each, show what it is, where it would go, and why
it recurs. Let the user approve all, approve some, or reject. Don't apply anything they didn't approve.

### 6. Apply the approved learnings
Edit the destination files to insert the approved learnings in the right section, in the format §9
specifies (e.g. append a bullet under `src/CONTEXT.md` "Patterns We Follow"; add a row to the
`CLAUDE.md` "Commands" table; create a dated ADR under `planning/decisions/`). A `thing-to-avoid`
goes under `CLAUDE.md` → Avoid → **Soft defaults** (never the Hard block — that's user-authored),
carrying today's date + `provenance: learned`, exactly as §9's insert format shows. Append a short
audit note to `.icm/LEARNINGS-INBOX.md` recording what was applied and when. Discard the rejected ones.

## Example

Session built a login form; you twice forgot to validate inputs and the user said "always validate
with zod"; you also renamed one file.
- "Always validate inputs with zod" → **new-convention**, recurs → keep → append to `src/CONTEXT.md`
  "Patterns We Follow": `- Validate all inputs with zod at the boundary: catches bad data early.`
- "Renamed auth.ts → session.ts" → one-off, does not recur → **discard.**

## What NOT to do
- Don't save one-offs, and don't pad the list — a short, high-signal set is the point.
- Don't apply anything without approval; don't touch L4 working files (code, specs).
- Don't modify the skills, the registry, or global config — project-local only.
