# src

## What This Workspace Is
The existing application code. Frontend: Next.js (React). Backend: Next.js API routes (Node). Data: Postgres (Prisma).
Lives in `src/app/` (routes/pages) and `src/lib/` (shared logic, e.g. the Prisma client in `lib/db.ts`).

## What to Load
| Task | Load These | Skip These |
|------|-----------|------------|
| Implement a feature | the spec from `../planning/specs/`, the relevant `app/` or `lib/` module | `docs/`, `ops/` |
| Fix a bug | this file's **Known Gotchas** first; then the failing module; `lib/db.ts` for data | unrelated specs |

## Patterns We Follow
- Build to the spec's acceptance criteria; verify before calling a feature done.

## Known Gotchas
<!-- Diagnostic memory: symptom → likely cause → fix/check. Check BEFORE debugging from scratch.
     session-learnings appends recurring gotchas below this line -->
- None recorded yet.

## Skills & Tools
| Skill / Tool | When | Purpose |
|--------------|------|---------|
| `superpowers:test-driven-development` | Before writing feature code | Tests first |
| `superpowers:systematic-debugging` | On any bug or unexpected behavior | Root-cause before fixing — after checking **Known Gotchas** above |
| Context7 MCP | Need current library docs mid-build | Fetch accurate API usage |

> Baseline skills for this project type. If one isn't installed, install it: superpowers → https://github.com/obra/superpowers · Context7 MCP → https://github.com/upstash/context7

## What NOT to Do
- Don't move or rename existing modules under `src/` — extend in place.
- Don't bypass the spec — if scope changes, update the spec first.
