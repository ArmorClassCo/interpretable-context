# src

## What This Workspace Is
The existing application code. Frontend: Next.js (React). Backend: Next.js API routes (Node). Data: Postgres (Prisma).
Lives in `src/app/` (routes/pages) and `src/lib/` (shared logic, e.g. the Prisma client in `lib/db.ts`).

## What to Load
| Task | Load These | Skip These |
|------|-----------|------------|
| Implement a feature | the spec from `../planning/specs/`, the relevant `app/` or `lib/` module | `docs/`, `ops/` |
| Fix a bug | the failing module; `lib/db.ts` for data | unrelated specs |

## Patterns We Follow
- Build to the spec's acceptance criteria; verify before calling a feature done.

## What NOT to Do
- Don't move or rename existing modules under `src/` — extend in place.
- Don't bypass the spec — if scope changes, update the spec first.
