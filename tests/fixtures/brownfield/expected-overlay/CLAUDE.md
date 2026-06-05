# Notesy — Project Map

## What This Is
Capture and organize personal notes.
Built for: People who want quick personal notes. Platform: web.

## Folder Structure
```
notesy/
├── CLAUDE.md            (ICM map)
├── CONTEXT.md           (ICM router)
├── .icm/
├── package.json         (existing)
├── next.config.js       (existing)
├── Dockerfile           (existing)
├── src/                 (existing app code: app/, lib/)
│   └── CONTEXT.md       (ICM contract)
├── docs/                (existing docs, incl. architecture/)
│   └── CONTEXT.md       (ICM contract)
├── planning/            (ICM-added)
│   └── CONTEXT.md
└── ops/                 (ICM-added; covers root Dockerfile)
    └── CONTEXT.md
```

## Naming Conventions
| Thing | Pattern | Example |
|-------|---------|---------|
| Feature spec | `planning/specs/{feature}-spec.md` | `notes-spec.md` |
| Decision (ADR) | `planning/decisions/YYYY-MM-DD_{title}.md` | `2026-06-01_pick-prisma.md` |
| Guide | `docs/guides/{slug}.md` | `local-setup.md` |
| Script | `ops/scripts/{verb}-{noun}.sh` | `seed-db.sh` |

## Commands
| Do this | Run |
|---------|-----|
| Install dependencies | npm install |
| Start locally | npm run dev |
| Run tests | TBD |
| Deploy | docker build . (self-hosted) |

## Avoid

### Hard constraints (never cross)
- Don't modify the existing `Dockerfile` or build pipeline without recording an ADR.
- Don't hard-code secrets or keys — use the host's secret store (Docker (self-hosted)).

### Soft defaults (revisit as the project matures)
- Stay within the agreed launch scope; don't add features beyond the current `planning/specs/` without writing a spec first. — default, 2026-06-05, provenance: scaffold-baseline
- Don't introduce tech or services outside the chosen stack (Next.js (React) / Next.js API routes (Node) / Postgres (Prisma)) without recording an ADR in `planning/decisions/`. — default, 2026-06-05, provenance: scaffold-baseline
- Don't refactor or modify areas unrelated to the current task — keep changes scoped. — default, 2026-06-05, provenance: scaffold-baseline

## Current State
- ICM overlaid on the existing repo 2026-06-05. No source files moved or modified.

## Maintenance
When a chunk of work looks finished, consider running the `session-learnings` skill to
capture any reusable learnings into this project's context files.
