# ToolShare — Project Map

## What This Is
Let neighbors lend and borrow tools.
Built for: Local residents who occasionally need a tool; main action is to list a tool or request a borrow. Platform: web.

## Folder Structure
```
ToolShare/
├── CLAUDE.md
├── CONTEXT.md
├── .icm/
├── planning/   (specs, architecture, decisions)
├── src/        (application code)
├── docs/       (api, guides, changelog)
└── ops/        (deploy, monitoring, scripts)
```

## Naming Conventions
| Thing | Pattern | Example |
|-------|---------|---------|
| Feature spec | `planning/specs/{feature}-spec.md` | `booking-flow-spec.md` |
| Decision (ADR) | `planning/decisions/YYYY-MM-DD_{title}.md` | `2026-06-01_pick-supabase.md` |
| Guide | `docs/guides/{slug}.md` | `local-setup.md` |
| Script | `ops/scripts/{verb}-{noun}.sh` | `seed-db.sh` |

## Commands
| Do this | Run |
|---------|-----|
| Install dependencies | npm install |
| Start locally | npm run dev |
| Run tests | TBD |
| Deploy | Push to main (Vercel auto-deploy) |

## Avoid

### Hard constraints (never cross)
- Don't add payments or checkout in v1.
- Don't store exact home addresses — neighborhood-level location only.
- Don't hard-code secrets or keys — use the host's secret store (Vercel).

### Soft defaults (revisit as the project matures)
- Prefer not to add a native mobile app until the web app is validated. — default, 2026-06-05, provenance: assumed-default
- Stay within the agreed launch scope; don't add features beyond the current `planning/specs/` without writing a spec first. — default, 2026-06-05, provenance: scaffold-baseline
- Don't introduce tech or services outside the chosen stack (Next.js (React) / Next.js API routes (Node) / Supabase (Postgres)) without recording an ADR in `planning/decisions/`. — default, 2026-06-05, provenance: scaffold-baseline
- Don't refactor or modify areas unrelated to the current task — keep changes scoped. — default, 2026-06-05, provenance: scaffold-baseline

## Current State
- Project scaffolded 2026-06-05. Nothing built yet.

## Maintenance
When a chunk of work looks finished, consider running the `session-learnings` skill to
capture any reusable learnings into this project's context files.
